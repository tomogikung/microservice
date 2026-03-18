# Multi-Language API Examples

This repository collects the same small API idea across multiple languages so they can be compared side by side.

Thai version: [README_TH.md](./README_TH.md)

Each project follows the same shape:
- `GET /`
- `GET /time`
- `GET /health`
- response with `status`, `trace_id`, `message`, `data`, `request`

## Comparison Table

| Language | Project | Dependency | Source | Execute / Output | Run | Port |
| --- | --- | --- | --- | --- | --- | --- |
| Rust | [`hello_rust`](./hello_rust/README) | `Cargo.toml` | `src/main.rs` | `target/debug/hello_rust` or `target/release/hello_rust` | `cargo run` | `3000` |
| Go | [`hello_go`](./hello_go/README.md) | `go.mod` | `main.go` | compiled binary such as `hello_go` | `go run .` | `3001` |
| Python | [`hello_python`](./hello_python/README.md) | `requirements.txt` | `main.py` | Python process started by `uvicorn` | `uvicorn main:app --reload --port 3002` | `3002` |
| JavaScript | [`hello_javascript`](./hello_javascript/README.md) | `package.json` | `server.js` | Node.js process started by `node` | `npm install && npm start` | `3003` |
| PHP | [`hello_php`](./hello_php/README.md) | `composer.json` | `public/index.php` | PHP process started by the built-in server | `php -S 127.0.0.1:3004 -t public` | `3004` |
| C# | [`hello_csharp`](./hello_csharp/README.md) | `hello_csharp.csproj` | `Program.cs` | `bin/Debug/net8.0/hello_csharp` or `bin/Release/net8.0/hello_csharp` | `dotnet run` | `3005` |
| Java | [`hello_java`](./hello_java/README.md) | `pom.xml` | `src/main/java/com/example/hello_java/` | `target/hello_java-0.1.0.jar` | `mvn spring-boot:run` | `3006` |
| Dart | [`hello_dart`](./hello_dart/README.md) | `pubspec.yaml` | `bin/main.dart` | Dart process started by `dart run` | `dart run bin/main.dart` | `3007` |
| Bash | [`hello_bash`](./hello_bash/README.md) | no package dependency file | `server.sh` | Bash process started by `bash` | `bash server.sh` | `3008` |

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

- Rust, Go, and Python are the easiest current candidates to run in this environment with the least extra setup.
- Java has a runtime available, but Maven is still missing.
- JavaScript, PHP, C#, and Dart are currently represented as project structure and reference examples until their runtimes are installed.
- Bash is present, but its sample server is intentionally very simple and mainly useful as a comparison project.

## Project Goal

The goal of this repository is not just to run one app in many languages, but to compare how each ecosystem thinks about:
- dependency files
- source layout
- build output
- run commands
- HTTP route structure
- JSON response design

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
