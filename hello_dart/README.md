# hello_dart

Dart API example using `dart:io`.

## Project Structure

- Dependency: `pubspec.yaml`
- Source: `bin/main.dart`
- Execute: Dart process started by `dart run`
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
- time and health responses

Current routes:
- `/` returns welcome information
- `/time` returns time data in UTC and Thailand time
- `/health` returns service health status

### Execute

Dart does not create a compiled executable in this basic setup.

The app runs as a Dart process through:

```bash
dart run bin/main.dart
```

## How `dart run bin/main.dart` Works

When you run:

```bash
dart run bin/main.dart
```

Dart works in this order:

1. Read `pubspec.yaml`
2. Load source code from `bin/main.dart`
3. Start the HTTP server
4. Listen for requests on `127.0.0.1:3007`

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
5. Dart converts the response into JSON
6. The API returns the JSON response to the client

## Run the Project

From the `hello_dart` directory:

```bash
dart run bin/main.dart
```

Then open:

- `http://127.0.0.1:3007/`
- `http://127.0.0.1:3007/time`
- `http://127.0.0.1:3007/health`

## Summary

- `pubspec.yaml` tells Dart about the project
- `bin/main.dart` contains the application logic
- `dart run` runs the API server
- this project uses port `3007`
