# Multi-Language API Examples

This repository collects the same small API idea across multiple languages so they can be compared side by side.

The first version of these projects focused on plain request-response APIs.

The current version pushes every `hello_*` service one step further into a starter event-driven shape.

Thai version: [README_TH.md](./README_TH.md)

Each project now follows the same high-level shape:
- `GET /`
- `GET /time`
- `GET /health`
- response with `status`, `trace_id`, `message`, `event_status`, `data`, `request`
- internal event publishing for every request
- consumed events written to `events/request-events.jsonl`

## Comparison Table

| Language | Project | Dependency | Source | Execute / Output | Run | Port | Event Pattern |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Rust | [`hello_rust`](./hello_rust/README) | `Cargo.toml` | `src/main.rs` | `target/debug/hello_rust` or `target/release/hello_rust` | `cargo run` | `3000` | `tokio` channel + background consumer |
| Go | [`hello_go`](./hello_go/README.md) | `go.mod` | `main.go` | compiled binary such as `hello_go` | `go run .` | `3001` | Go channel + goroutine consumer |
| Python | [`hello_python`](./hello_python/README.md) | `requirements.txt` | `main.py` | Python process started by `uvicorn` | `uvicorn main:app --reload --port 3002` | `3002` | `asyncio.Queue` + async consumer |
| JavaScript | [`hello_javascript`](./hello_javascript/README.md) | `package.json` | `server.js` | Node.js process started by `node` | `npm install && npm start` | `3003` | in-memory queue + async file logger |
| PHP | [`hello_php`](./hello_php/README.md) | `composer.json` | `public/index.php` | PHP process started by the built-in server | `php -S 127.0.0.1:3004 -t public` | `3004` | file outbox + `consumer.php` |
| C# | [`hello_csharp`](./hello_csharp/README.md) | `hello_csharp.csproj` | `Program.cs` | `bin/Debug/net8.0/hello_csharp` or `bin/Release/net8.0/hello_csharp` | `dotnet run` | `3005` | `Channel<AppEvent>` + `BackgroundService` |
| Java | [`hello_java`](./hello_java/README.md) | `pom.xml` | `src/main/java/com/example/hello_java/` | `target/hello_java-0.1.0.jar` | `mvn spring-boot:run` | `3006` | blocking queue + background consumer thread |
| Dart | [`hello_dart`](./hello_dart/README.md) | `pubspec.yaml` | `bin/main.dart` | Dart process started by `dart run` | `dart run bin/main.dart` | `3007` | `StreamController` + async consumer |
| Bash | [`hello_bash`](./hello_bash/README.md) | no package dependency file | `server.sh` | Bash process started by `bash` | `bash server.sh` | `3008` | file queue + background loop |

## Event-Driven Summary

All projects now follow the same comparison flow:

1. client sends HTTP request
2. route handler builds the JSON response
3. route handler publishes an internal event
4. a consumer processes that event in the background
5. the consumed event is stored in `events/request-events.jsonl`

The shared goal is comparison, not perfect production parity.

That is why each language uses the event mechanism that best fits its runtime model instead of forcing one identical implementation everywhere.

## Verification Status

| Language | Status |
| --- | --- |
| Rust | live request and event log verified |
| Go | live request and event log verified |
| Python | live request and event log verified |
| JavaScript | code and README updated, runtime not installed in this machine |
| PHP | code and README updated, runtime not installed in this machine |
| C# | code and README updated, runtime not installed in this machine |
| Java | code and README updated, `java` present but `mvn` missing |
| Dart | code and README updated, runtime not installed in this machine |
| Bash | script syntax checked with `bash -n` |

## Local Runtime Status

These are the runtimes and tools detected in this machine at the moment:

| Tool | Status |
| --- | --- |
| `cargo` | available |
| `go` | available |
| `python3` | available |
| `node` | not found |
| `php` | not found |
| `dotnet` | not found |
| `java` | available |
| `dart` | not found |
| `bash` | available |
| `mvn` | not found |

## Notes

- Rust, Go, and Python are the strongest current examples because their event-driven flow was verified end to end.
- Java has a runtime available, but Maven is still missing, so the Spring Boot example is prepared but not executed here.
- JavaScript, PHP, C#, and Dart already include the event-driven code structure, but they still need their runtimes installed before they can be verified in this machine.
- Bash is intentionally minimal, but it still demonstrates producer, queue, consumer, and JSONL event output clearly.

## Project Goal

The goal of this repository is not just to run one app in many languages, but to compare how each ecosystem thinks about:
- dependency files
- source layout
- build output
- run commands
- HTTP route structure
- JSON response design
- internal event publishing
- background event consumption
- runtime-friendly event patterns

## Recommended Reading Order

If you want a practical learning path, this sequence works well:

1. Rust
2. Go
3. Python
4. JavaScript
5. PHP
6. C#
7. Java
8. Dart
9. Bash
