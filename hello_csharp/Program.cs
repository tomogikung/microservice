using System.Globalization;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

static object RequestInfo(HttpRequest request, string traceId) => new
{
    method = request.Method,
    path = request.Path.ToString(),
    trace_id = traceId
};

app.MapGet("/", (HttpRequest request) =>
{
    var traceId = Guid.NewGuid().ToString();

    return Results.Json(new
    {
        status = "success",
        trace_id = traceId,
        message = "Welcome to hello_csharp API",
        data = new
        {
            service = "hello_csharp",
            version = "0.1.0",
            available_routes = new[] { "/", "/time", "/health" }
        },
        request = RequestInfo(request, traceId)
    });
});

app.MapGet("/time", (HttpRequest request) =>
{
    var traceId = Guid.NewGuid().ToString();
    var nowUtc = DateTimeOffset.UtcNow;
    var thailand = TimeZoneInfo.CreateCustomTimeZone(
        "Asia/Bangkok",
        TimeSpan.FromHours(7),
        "Asia/Bangkok",
        "Asia/Bangkok");
    var nowTh = TimeZoneInfo.ConvertTime(nowUtc, thailand);

    return Results.Json(new
    {
        status = "success",
        trace_id = traceId,
        message = "Current server time",
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

app.MapGet("/health", (HttpRequest request) =>
{
    var traceId = Guid.NewGuid().ToString();

    return Results.Json(new
    {
        status = "success",
        trace_id = traceId,
        message = "Service is healthy",
        data = new
        {
            service = "hello_csharp",
            healthy = true
        },
        request = RequestInfo(request, traceId)
    });
});

app.Run("http://127.0.0.1:3005");
