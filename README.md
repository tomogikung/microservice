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

## `ex_file` Usage Guide

ไฟล์ `ex_file` ในโปรเจกต์นี้ใช้เป็นเอกสารประกอบการเรียนรู้ Docker image ของแต่ละ microservice โดยสรุปว่า service นั้นควรมี `Dockerfile` แบบไหน ใช้คำสั่ง build อะไร ต้องมีไฟล์อะไรใน build context และตอนรันจริง container จะมีโครงสร้างประมาณใด

ไฟล์นี้ไม่ได้เป็นสคริปต์สำหรับรันโดยตรง แต่เป็น reference สำหรับอ่าน เปรียบเทียบ และนำไปสร้างหรือทบทวน `Dockerfile`

### ตำแหน่งไฟล์

มี `ex_file` อยู่ 2 ระดับหลัก:

| ตำแหน่ง | ใช้สำหรับ |
| --- | --- |
| `microservice/ex_file` | ตัวอย่าง Dockerfile ของโปรเจกต์ `Muti` หรือ Rust Axum service |
| `microservice/hello_*/ex_file` | ตัวอย่าง Dockerfile และคำอธิบายของ service แต่ละภาษา |

ตัวอย่างไฟล์ที่มีในโปรเจกต์:

| Service | ไฟล์ |
| --- | --- |
| Rust | `hello_rust/ex_file` |
| Go | `hello_go/ex_file` |
| Python | `hello_python/ex_file` |
| JavaScript | `hello_javascript/ex_file` |
| PHP | `hello_php/ex_file` |
| C# | `hello_csharp/ex_file` |
| Java | `hello_java/ex_file` |
| Dart | `hello_dart/ex_file` |
| Bash | `hello_bash/ex_file` |

### โครงสร้างเนื้อหาใน `ex_file`

แต่ละไฟล์มักแบ่งเป็นหัวข้อประมาณนี้:

| หัวข้อ | ความหมาย |
| --- | --- |
| `1. Real World` | ตัวอย่าง Dockerfile ที่ควรใช้จริง |
| `2. Command` | คำสั่งสำหรับ build Docker image |
| `3. Context` | ไฟล์หรือโฟลเดอร์ที่ต้องอยู่ใน build context |
| `4. Build stage` | รายละเอียด stage ที่ใช้ build หรือเตรียม dependency |
| `5. Runtime stage` | รายละเอียด image สุดท้ายที่ใช้ตอนรันจริง |
| `6. Real World line by line` | คำอธิบาย Dockerfile ทีละบรรทัด บาง service มีหัวข้อนี้ |

### วิธีใช้งานพื้นฐาน

เข้าไปที่โฟลเดอร์ `microservice` ก่อน:

```bash
cd microservice
```

เลือก service ที่ต้องการดู เช่น Python:

```bash
cd hello_python
```

เปิดอ่าน `ex_file` เพื่อดู Dockerfile ตัวอย่างและคำสั่ง build:

```bash
cat ex_file
```

จากนั้นตรวจว่าโฟลเดอร์นั้นมี `Dockerfile` และไฟล์ในหัวข้อ `Context` ครบ เช่น:

```bash
ls
```

ถ้าต้องการ build image ให้ใช้คำสั่งในหัวข้อ `2. Command` เช่น:

```bash
docker build -t hello-python .
```

### วิธีรัน container หลัง build

หลัง build image แล้ว สามารถรัน container โดย map port ออกมาที่เครื่อง host ได้ เช่น Python service ใช้ port `3002`:

```bash
docker run --rm -p 3002:3002 hello-python
```

จากนั้นทดสอบ endpoint:

```bash
curl http://127.0.0.1:3002/
curl http://127.0.0.1:3002/time
curl http://127.0.0.1:3002/health
```

สำหรับ service อื่นให้เปลี่ยนชื่อ image และ port ตามตารางนี้:

| Service | Image name จาก `ex_file` | Port |
| --- | --- | --- |
| Rust | `hello-rust` | `3000` |
| Go | `hello-go` | `3001` |
| Python | `hello-python` | `3002` |
| JavaScript | `hello-javascript` | `3003` |
| PHP | `hello-php` | `3004` |
| C# | `hello-csharp` | `3005` |
| Java | `hello-java` | `3006` |
| Dart | `hello-dart` | `3007` |
| Bash | `hello-bash` | `3008` |
| Muti | `muti-axum` | `3009` |

ตัวอย่างการรัน Go service:

```bash
cd microservice/hello_go
docker build -t hello-go .
docker run --rm -p 3001:3001 hello-go
```

### การอ่าน Build stage และ Runtime stage

หลาย service ใช้ multi-stage build:

1. `Build stage` ใช้ image ที่มี compiler หรือ SDK เช่น `rust`, `golang`, `maven`, `dotnet/sdk`
2. `Runtime stage` ใช้ image ที่เล็กกว่า เช่น `debian:bookworm-slim`, `aspnet`, `jre`
3. ไฟล์ที่ build เสร็จแล้วจะถูก copy จาก build stage ไป runtime stage ด้วย `COPY --from=builder`

แนวคิดนี้ช่วยให้ image สุดท้ายเล็กลง และไม่ต้องมีเครื่องมือ build อยู่ใน container ตอน production

### การใช้งานกับ event log

service ส่วนใหญ่ในโปรเจกต์นี้มี event-driven flow โดยจะเขียน event ที่ consume แล้วลงไฟล์:

```text
events/request-events.jsonl
```

บาง service ต้องสร้างโฟลเดอร์ `events` หรือ `events/pending` ใน Dockerfile และตั้งสิทธิ์ให้ user ที่รัน service เขียนไฟล์ได้ ตัวอย่างเช่น:

```dockerfile
RUN mkdir -p /app/events \
    && chown -R appuser:appuser /app
```

ถ้ารัน container แล้วต้องการดู event log ภายใน container ให้เปิด shell เข้าไปตรวจได้ เช่น:

```bash
docker exec -it <container_name_or_id> sh
cat /app/events/request-events.jsonl
```

### แนวทางเมื่อเพิ่ม service ใหม่

ถ้าจะเพิ่ม microservice ภาษาใหม่ ให้ทำตามรูปแบบนี้:

1. สร้างโฟลเดอร์ใหม่ เช่น `hello_newlang`
2. ใส่ source code หลักและไฟล์ dependency ของภาษานั้น
3. สร้าง `Dockerfile`
4. สร้าง `ex_file` เพื่ออธิบาย Dockerfile ตามหัวข้อเดียวกับ service อื่น
5. ระบุ command build, context, build stage, runtime stage และคำอธิบาย line by line
6. อัปเดต `README.md` และ `README_TH.md` ถ้าต้องการให้ service แสดงในตารางรวม

### ข้อควรระวัง

- ต้องรัน `docker build` จากโฟลเดอร์ของ service นั้น เพราะ build context จะอ้างอิงไฟล์ในโฟลเดอร์ปัจจุบัน
- ถ้า Dockerfile ใช้ `COPY` ไฟล์ใด ไฟล์นั้นต้องอยู่ใน build context จริง
- port ใน `docker run -p host:container` ควรตรงกับ `ENV PORT` และ `EXPOSE` ของ service
- service ที่เขียน event log ต้องมี permission เขียนไฟล์ใน `/app/events`
- ถ้าใช้ multi-stage build ชื่อไฟล์ output ต้องตรงกับไฟล์ที่ `COPY --from=builder` อ้างถึง
