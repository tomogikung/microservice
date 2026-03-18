<?php

declare(strict_types=1);

$path = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH) ?: '/';
$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
$traceId = bin2hex(random_bytes(16));

function request_info(string $method, string $path, string $traceId): array
{
    return [
        'method' => $method,
        'path' => $path,
        'trace_id' => $traceId,
    ];
}

function json_response(array $payload): void
{
    header('Content-Type: application/json');
    echo json_encode($payload, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
}

if ($path === '/') {
    json_response([
        'status' => 'success',
        'trace_id' => $traceId,
        'message' => 'Welcome to hello_php API',
        'data' => [
            'service' => 'hello_php',
            'version' => '0.1.0',
            'available_routes' => ['/', '/time', '/health'],
        ],
        'request' => request_info($method, $path, $traceId),
    ]);
    return;
}

if ($path === '/time') {
    $utc = new DateTimeImmutable('now', new DateTimeZone('UTC'));
    $th = $utc->setTimezone(new DateTimeZone('Asia/Bangkok'));

    json_response([
        'status' => 'success',
        'trace_id' => $traceId,
        'message' => 'Current server time',
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
    json_response([
        'status' => 'success',
        'trace_id' => $traceId,
        'message' => 'Service is healthy',
        'data' => [
            'service' => 'hello_php',
            'healthy' => true,
        ],
        'request' => request_info($method, $path, $traceId),
    ]);
    return;
}

http_response_code(404);
json_response([
    'status' => 'error',
    'trace_id' => $traceId,
    'message' => 'Route not found',
    'data' => null,
    'request' => request_info($method, $path, $traceId),
]);
