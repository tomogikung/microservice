import 'dart:async';
import 'dart:convert';
import 'dart:io';

const serviceName = 'hello_dart';
const defaultHost = '127.0.0.1';
const defaultPort = 3007;
const eventLogPath = 'events/request-events.jsonl';

String newTraceId() => DateTime.now().toUtc().microsecondsSinceEpoch.toString();

Map<String, dynamic> requestInfo(HttpRequest request, String traceId) {
  return {
    'method': request.method,
    'path': request.uri.path,
    'trace_id': traceId,
  };
}

Future<void> sendJson(HttpResponse response, Map<String, dynamic> payload) async {
  response.headers.contentType = ContentType.json;
  response.write(jsonEncode(payload));
  await response.close();
}

Map<String, dynamic> buildEvent(
  HttpRequest request,
  String eventType,
  String traceId,
  String responseMessage,
) {
  final nowUtc = DateTime.now().toUtc();

  return {
    'event_id': newTraceId(),
    'event_type': eventType,
    'emitted_at_utc': nowUtc.toIso8601String(),
    'service': serviceName,
    'trace_id': traceId,
    'request': requestInfo(request, traceId),
    'data': {
      'route': request.uri.path,
      'response_message': responseMessage,
      'response_timestamp': nowUtc.millisecondsSinceEpoch ~/ 1000,
    },
  };
}

String publishEvent(
  StreamController<Map<String, dynamic>> eventController,
  HttpRequest request,
  String eventType,
  String traceId,
  String responseMessage,
) {
  if (eventController.isClosed) {
    return 'dropped';
  }

  eventController.add(
    buildEvent(request, eventType, traceId, responseMessage),
  );

  return 'queued';
}

Future<void> eventConsumer(Stream<Map<String, dynamic>> events) async {
  final eventLogFile = File(eventLogPath);
  await eventLogFile.parent.create(recursive: true);

  await for (final event in events) {
    await eventLogFile.writeAsString(
      '${jsonEncode(event)}\n',
      mode: FileMode.append,
      flush: true,
    );
  }
}

Future<void> main() async {
  final eventController = StreamController<Map<String, dynamic>>();
  unawaited(eventConsumer(eventController.stream));

  final host = Platform.environment['APP_HOST'] ?? defaultHost;
  final port = int.tryParse(Platform.environment['PORT'] ?? '') ?? defaultPort;
  final server = await HttpServer.bind(host, port);
  stdout.writeln('Server running at http://$host:$port');

  await for (final request in server) {
    final traceId = newTraceId();
    final path = request.uri.path;
    final nowUtc = DateTime.now().toUtc();
    final nowTh = nowUtc.add(const Duration(hours: 7));

    if (path == '/') {
      final eventStatus = publishEvent(
        eventController,
        request,
        'root_requested',
        traceId,
        'Welcome to hello_dart API',
      );

      await sendJson(request.response, {
        'status': 'success',
        'trace_id': traceId,
        'message': 'Welcome to hello_dart API',
        'event_status': eventStatus,
        'data': {
          'service': serviceName,
          'version': '0.1.0',
          'architecture': 'request-response + event consumer',
          'event_log_file': eventLogPath,
          'available_routes': ['/', '/time', '/health'],
        },
        'request': requestInfo(request, traceId),
      });
      continue;
    }

    if (path == '/time') {
      final eventStatus = publishEvent(
        eventController,
        request,
        'time_requested',
        traceId,
        'Current server time',
      );

      await sendJson(request.response, {
        'status': 'success',
        'trace_id': traceId,
        'message': 'Current server time',
        'event_status': eventStatus,
        'data': {
          'timestamp': nowUtc.millisecondsSinceEpoch ~/ 1000,
          'datetime_utc': nowUtc.toIso8601String(),
          'datetime_th': nowTh.toIso8601String(),
          'timezone': 'Asia/Bangkok',
          'utc_offset': '+07:00',
        },
        'request': requestInfo(request, traceId),
      });
      continue;
    }

    if (path == '/health') {
      final eventStatus = publishEvent(
        eventController,
        request,
        'health_requested',
        traceId,
        'Service is healthy',
      );

      await sendJson(request.response, {
        'status': 'success',
        'trace_id': traceId,
        'message': 'Service is healthy',
        'event_status': eventStatus,
        'data': {
          'service': serviceName,
          'healthy': true,
          'event_consumer': 'stream file logger',
          'port': port,
        },
        'request': requestInfo(request, traceId),
      });
      continue;
    }

    final eventStatus = publishEvent(
      eventController,
      request,
      'route_not_found',
      traceId,
      'Route not found',
    );

    request.response.statusCode = HttpStatus.notFound;
    await sendJson(request.response, {
      'status': 'error',
      'trace_id': traceId,
      'message': 'Route not found',
      'event_status': eventStatus,
      'data': null,
      'request': requestInfo(request, traceId),
    });
  }
}
