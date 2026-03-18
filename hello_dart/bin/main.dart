import 'dart:convert';
import 'dart:io';

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

Future<void> main() async {
  final server = await HttpServer.bind(InternetAddress.loopbackIPv4, 3007);
  stdout.writeln('Server running at http://127.0.0.1:3007');

  await for (final request in server) {
    final traceId = newTraceId();
    final path = request.uri.path;
    final nowUtc = DateTime.now().toUtc();
    final nowTh = nowUtc.add(const Duration(hours: 7));

    if (path == '/') {
      await sendJson(request.response, {
        'status': 'success',
        'trace_id': traceId,
        'message': 'Welcome to hello_dart API',
        'data': {
          'service': 'hello_dart',
          'version': '0.1.0',
          'available_routes': ['/', '/time', '/health'],
        },
        'request': requestInfo(request, traceId),
      });
      continue;
    }

    if (path == '/time') {
      await sendJson(request.response, {
        'status': 'success',
        'trace_id': traceId,
        'message': 'Current server time',
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
      await sendJson(request.response, {
        'status': 'success',
        'trace_id': traceId,
        'message': 'Service is healthy',
        'data': {
          'service': 'hello_dart',
          'healthy': true,
        },
        'request': requestInfo(request, traceId),
      });
      continue;
    }

    request.response.statusCode = HttpStatus.notFound;
    await sendJson(request.response, {
      'status': 'error',
      'trace_id': traceId,
      'message': 'Route not found',
      'data': null,
      'request': requestInfo(request, traceId),
    });
  }
}
