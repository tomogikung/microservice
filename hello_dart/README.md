# hello_dart

Dart API example using `dart:io`.

Default port: `127.0.0.1:3007`

## Project Structure

- Dependency: `pubspec.yaml`
- Source: `bin/main.dart`
- Execute: Dart process started by `dart run`
- Event log: `events/request-events.jsonl`
- Run: `dart run bin/main.dart`

## What Each File Does

### `pubspec.yaml`

This is the dependency and project configuration file.

It defines:
- project name
- version
- Dart SDK requirement

In this project, `pubspec.yaml` is minimal because the API uses Dart core libraries.

### `bin/main.dart`

This is the main source file of the project.

It contains:
- HTTP server setup
- JSON response helper
- request metadata helper
- internal event publishing
- background event consumer
- time and health responses

Current routes:
- `/` returns welcome information
- `/time` returns time data in UTC and Thailand time
- `/health` returns service health status

Current event behavior:
- every request publishes an event into an internal Dart stream
- a background consumer reads queued events
- consumed events are appended to `events/request-events.jsonl`

### Execute

Dart does not create a compiled executable in this basic setup.

The app runs as a Dart process through:

```bash
dart run bin/main.dart
```

## Event-Driven Shape

This project now uses a simple event-driven pattern inside the service.

The HTTP handler still responds to the client immediately, but it also publishes an internal event.

That event is then consumed by a background worker.

Flow:

1. client sends request
2. route handler creates response data
3. route handler publishes an event into an internal stream
4. background consumer receives the event
5. event is written to `events/request-events.jsonl`

This is not a full broker-based event-driven architecture yet, but it is a clear first step toward one.

## How `dart run bin/main.dart` Works

When you run:

```bash
dart run bin/main.dart
```

Dart works in this order:

1. Read `pubspec.yaml`
2. Load source code from `bin/main.dart`
3. Start the background event consumer
4. Start the HTTP server
5. Listen for requests on `127.0.0.1:3007`

## Request Flow in This Project

When a browser or client calls:

```text
GET http://127.0.0.1:3007/time
```

the flow is:

1. Dart receives the request
2. The server checks the path `/time`
3. The `/time` branch is selected
4. The code creates:
   - UTC time
   - Thailand time
   - `trace_id`
   - request metadata
5. The handler publishes a `time_requested` event into the internal stream
6. Dart converts the response into JSON
7. The API returns the JSON response to the client
8. the background consumer writes the event into `events/request-events.jsonl`

## Run the Project

From the `hello_dart` directory:

```bash
dart run bin/main.dart
```

Then open:

- `http://127.0.0.1:3007/`
- `http://127.0.0.1:3007/time`
- `http://127.0.0.1:3007/health`

After calling the API, you can inspect:

```text
events/request-events.jsonl
```

to see the emitted events.

## Summary

- `pubspec.yaml` tells Dart about the project
- `bin/main.dart` contains the application logic
- `events/request-events.jsonl` stores consumed events
- `dart run` runs the API server
- this project uses port `3007`
