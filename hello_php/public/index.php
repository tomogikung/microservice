<?php

declare(strict_types=1);

const SERVICE_NAME = 'hello_php';
const DEFAULT_PORT = 3004;
const EVENT_QUEUE_DIR = __DIR__ . '/../events/pending';
const EVENT_LOG_FILE = 'events/request-events.jsonl';
const EVENT_QUEUE_PATH = 'events/pending';

$path = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH) ?: '/';
$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
$traceId = bin2hex(random_bytes(16));
$port = (int) (getenv('PORT') !== false ? getenv('PORT') : (string) DEFAULT_PORT);

function new_id(): string
{
    return bin2hex(random_bytes(16));
}

function request_info(string $method, string $path, string $traceId): array
{
    return [
        'method' => $method,
        'path' => $path,
        'trace_id' => $traceId,
    ];
}

function json_response(array $payload, int $statusCode = 200): void
{
    http_response_code($statusCode);
    header('Content-Type: application/json');
    echo json_encode($payload, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
}

function build_event(
    string $method,
    string $path,
    string $traceId,
    string $eventType,
    string $responseMessage
): array {
    $utc = new DateTimeImmutable('now', new DateTimeZone('UTC'));

    return [
        'event_id' => new_id(),
        'event_type' => $eventType,
        'emitted_at_utc' => $utc->format(DateTimeInterface::ATOM),
        'service' => SERVICE_NAME,
        'trace_id' => $traceId,
        'request' => request_info($method, $path, $traceId),
        'data' => [
            'route' => $path,
            'response_message' => $responseMessage,
            'response_timestamp' => $utc->getTimestamp(),
        ],
    ];
}

function publish_event(
    string $method,
    string $path,
    string $traceId,
    string $eventType,
    string $responseMessage
): string {
    if (!is_dir(EVENT_QUEUE_DIR) && !mkdir(EVENT_QUEUE_DIR, 0775, true) && !is_dir(EVENT_QUEUE_DIR)) {
        return 'dropped';
    }

    $event = build_event($method, $path, $traceId, $eventType, $responseMessage);
    $eventFile = sprintf('%s/%s.json', EVENT_QUEUE_DIR, $event['event_id']);
    $eventJson = json_encode($event, JSON_UNESCAPED_SLASHES);

    if ($eventJson === false) {
        return 'dropped';
    }

    $written = file_put_contents($eventFile, $eventJson . PHP_EOL, LOCK_EX);

    return $written === false ? 'dropped' : 'queued';
}

if ($path === '/') {
    $eventStatus = publish_event($method, $path, $traceId, 'root_requested', 'Welcome to hello_php API');

    json_response([
        'status' => 'success',
        'trace_id' => $traceId,
        'message' => 'Welcome to hello_php API',
        'event_status' => $eventStatus,
        'data' => [
            'service' => SERVICE_NAME,
            'version' => '0.1.0',
            'architecture' => 'request-response + outbox consumer',
            'event_queue_dir' => EVENT_QUEUE_PATH,
            'event_log_file' => EVENT_LOG_FILE,
            'available_routes' => ['/', '/time', '/health'],
        ],
        'request' => request_info($method, $path, $traceId),
    ]);
    return;
}

if ($path === '/time') {
    $utc = new DateTimeImmutable('now', new DateTimeZone('UTC'));
    $th = $utc->setTimezone(new DateTimeZone('Asia/Bangkok'));
    $eventStatus = publish_event($method, $path, $traceId, 'time_requested', 'Current server time');

    json_response([
        'status' => 'success',
        'trace_id' => $traceId,
        'message' => 'Current server time',
        'event_status' => $eventStatus,
        'data' => [
            'timestamp' => $utc->getTimestamp(),
            'datetime_utc' => $utc->format(DateTimeInterface::ATOM),
            'datetime_th' => $th->format(DateTimeInterface::ATOM),
            'timezone' => 'Asia/Bangkok',
            'utc_offset' => '+07:00',
        ],
        'request' => request_info($method, $path, $traceId),
    ]);
    return;
}

if ($path === '/health') {
    $eventStatus = publish_event($method, $path, $traceId, 'health_requested', 'Service is healthy');

    json_response([
        'status' => 'success',
        'trace_id' => $traceId,
        'message' => 'Service is healthy',
        'event_status' => $eventStatus,
        'data' => [
            'service' => SERVICE_NAME,
            'healthy' => true,
            'event_consumer' => 'consumer.php outbox processor',
            'port' => $port,
        ],
        'request' => request_info($method, $path, $traceId),
    ]);
    return;
}

$eventStatus = publish_event($method, $path, $traceId, 'route_not_found', 'Route not found');

json_response([
    'status' => 'error',
    'trace_id' => $traceId,
    'message' => 'Route not found',
    'event_status' => $eventStatus,
    'data' => null,
    'request' => request_info($method, $path, $traceId),
], 404);
