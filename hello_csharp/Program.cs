using System.Globalization;
using System.Text.Json;
using System.Threading.Channels;
using Microsoft.AspNetCore.Mvc;

const string ServiceName = "hello_csharp";
const string EventLogFile = "events/request-events.jsonl";
const int DefaultPort = 3005;

var host = Environment.GetEnvironmentVariable("APP_HOST") ?? "127.0.0.1";
var port = int.TryParse(Environment.GetEnvironmentVariable("PORT"), out var configuredPort)
    ? configuredPort
    : DefaultPort;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddSingleton(
    Channel.CreateBounded<AppEvent>(
        new BoundedChannelOptions(128)
        {
            SingleReader = true,
            SingleWriter = false,
            FullMode = BoundedChannelFullMode.DropWrite
        }));
builder.Services.AddHostedService<EventConsumerService>();

var app = builder.Build();

app.MapGet("/", (HttpRequest request, [FromServices] Channel<AppEvent> eventChannel) =>
{
    var traceId = Guid.NewGuid().ToString();
    var eventStatus = PublishEvent(eventChannel, request, "root_requested", traceId, "Welcome to hello_csharp API");

    return Results.Json(new
    {
        status = "success",
        trace_id = traceId,
        message = "Welcome to hello_csharp API",
        event_status = eventStatus,
        data = new
        {
            service = ServiceName,
            version = "0.1.0",
            architecture = "request-response + event consumer",
            event_log_file = EventLogFile,
            available_routes = new[] { "/", "/time", "/health" }
        },
        request = RequestInfo(request, traceId)
    });
});

app.MapGet("/time", (HttpRequest request, [FromServices] Channel<AppEvent> eventChannel) =>
{
    var traceId = Guid.NewGuid().ToString();
    var nowUtc = DateTimeOffset.UtcNow;
    var thailand = ThailandTimeZone();
    var nowTh = TimeZoneInfo.ConvertTime(nowUtc, thailand);
    var eventStatus = PublishEvent(eventChannel, request, "time_requested", traceId, "Current server time");

    return Results.Json(new
    {
        status = "success",
        trace_id = traceId,
        message = "Current server time",
        event_status = eventStatus,
        data = new
        {
            timestamp = nowUtc.ToUnixTimeSeconds(),
            datetime_utc = nowUtc.ToString("O", CultureInfo.InvariantCulture),
            datetime_th = nowTh.ToString("O", CultureInfo.InvariantCulture),
            timezone = "Asia/Bangkok",
            utc_offset = "+07:00"
        },
        request = RequestInfo(request, traceId)
    });
});

app.MapGet("/health", (HttpRequest request, [FromServices] Channel<AppEvent> eventChannel) =>
{
    var traceId = Guid.NewGuid().ToString();
    var eventStatus = PublishEvent(eventChannel, request, "health_requested", traceId, "Service is healthy");

    return Results.Json(new
    {
        status = "success",
        trace_id = traceId,
        message = "Service is healthy",
        event_status = eventStatus,
        data = new
        {
            service = ServiceName,
            healthy = true,
            event_consumer = "background service file logger",
            port
        },
        request = RequestInfo(request, traceId)
    });
});

app.Run($"http://{host}:{port}");

static RequestInfo RequestInfo(HttpRequest request, string traceId) => new(
    request.Method,
    request.Path.ToString(),
    traceId);

static string PublishEvent(
    Channel<AppEvent> eventChannel,
    HttpRequest request,
    string eventType,
    string traceId,
    string responseMessage)
{
    var appEvent = new AppEvent(
        Guid.NewGuid().ToString(),
        eventType,
        DateTimeOffset.UtcNow.ToString("O", CultureInfo.InvariantCulture),
        ServiceName,
        traceId,
        RequestInfo(request, traceId),
        new EventData(
            request.Path.ToString(),
            responseMessage,
            DateTimeOffset.UtcNow.ToUnixTimeSeconds()));

    return eventChannel.Writer.TryWrite(appEvent) ? "queued" : "dropped";
}

static TimeZoneInfo ThailandTimeZone() => TimeZoneInfo.CreateCustomTimeZone(
    "Asia/Bangkok",
    TimeSpan.FromHours(7),
    "Asia/Bangkok",
    "Asia/Bangkok");

public sealed record RequestInfo(string method, string path, string trace_id);

public sealed record EventData(string route, string response_message, long response_timestamp);

public sealed record AppEvent(
    string event_id,
    string event_type,
    string emitted_at_utc,
    string service,
    string trace_id,
    RequestInfo request,
    EventData data);

public sealed class EventConsumerService(
    Channel<AppEvent> eventChannel,
    IHostEnvironment hostEnvironment,
    ILogger<EventConsumerService> logger) : BackgroundService
{
    private readonly Channel<AppEvent> _eventChannel = eventChannel;
    private readonly IHostEnvironment _hostEnvironment = hostEnvironment;
    private readonly ILogger<EventConsumerService> _logger = logger;

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        var eventsDirectory = Path.Combine(_hostEnvironment.ContentRootPath, "events");
        var eventLogPath = Path.Combine(eventsDirectory, "request-events.jsonl");

        Directory.CreateDirectory(eventsDirectory);

        await foreach (var appEvent in _eventChannel.Reader.ReadAllAsync(stoppingToken))
        {
            try
            {
                var jsonLine = JsonSerializer.Serialize(appEvent) + Environment.NewLine;
                await File.AppendAllTextAsync(eventLogPath, jsonLine, stoppingToken);
            }
            catch (OperationCanceledException) when (stoppingToken.IsCancellationRequested)
            {
                break;
            }
            catch (Exception exception)
            {
                _logger.LogError(exception, "Failed to write event log entry");
            }
        }
    }
}
