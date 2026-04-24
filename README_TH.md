# ตัวอย่าง API หลายภาษา

repository นี้รวบรวมโปรเจกต์ API แนวคิดเดียวกันในหลายภาษา เพื่อให้เปรียบเทียบกันได้แบบตรง ๆ

เวอร์ชันแรกของโปรเจกต์เหล่านี้เน้น API แบบ request-response ธรรมดา

เวอร์ชันปัจจุบันยกทุก `hello_*` ไปอีกขั้น ให้มีรูปแบบ event-driven ตั้งต้นเพิ่มเข้ามาด้วย

ไฟล์ภาษาอังกฤษ: [README.md](./README.md)

ตอนนี้แต่ละโปรเจกต์มีรูปแบบหลักร่วมกันดังนี้:
- `GET /`
- `GET /time`
- `GET /health`
- response มี `status`, `trace_id`, `message`, `event_status`, `data`, `request`
- ทุก request มีการ publish event ภายใน
- event ที่ถูก consume แล้วจะถูกเก็บใน `events/request-events.jsonl`

## ตารางเปรียบเทียบ

| ภาษา | โปรเจกต์ | ไฟล์ Dependency | ไฟล์ Source | ไฟล์ Execute / Output | คำสั่ง Run | Port | รูปแบบ Event |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Rust | [`hello_rust`](./hello_rust/README) | `Cargo.toml` | `src/main.rs` | `target/debug/hello_rust` หรือ `target/release/hello_rust` | `cargo run` | `3000` | `tokio` channel + background consumer |
| Go | [`hello_go`](./hello_go/README.md) | `go.mod` | `main.go` | binary ที่ build ออกมา เช่น `hello_go` | `go run .` | `3001` | Go channel + goroutine consumer |
| Python | [`hello_python`](./hello_python/README.md) | `requirements.txt` | `main.py` | Python process ที่รันผ่าน `uvicorn` | `uvicorn main:app --reload --port 3002` | `3002` | `asyncio.Queue` + async consumer |
| JavaScript | [`hello_javascript`](./hello_javascript/README.md) | `package.json` | `server.js` | Node.js process ที่รันผ่าน `node` | `npm install && npm start` | `3003` | in-memory queue + async file logger |
| PHP | [`hello_php`](./hello_php/README.md) | `composer.json` | `public/index.php` | PHP process ที่รันผ่าน built-in server | `php -S 127.0.0.1:3004 -t public` | `3004` | file outbox + `consumer.php` |
| C# | [`hello_csharp`](./hello_csharp/README.md) | `hello_csharp.csproj` | `Program.cs` | `bin/Debug/net8.0/hello_csharp` หรือ `bin/Release/net8.0/hello_csharp` | `dotnet run` | `3005` | `Channel<AppEvent>` + `BackgroundService` |
| Java | [`hello_java`](./hello_java/README.md) | `pom.xml` | `src/main/java/com/example/hello_java/` | `target/hello_java-0.1.0.jar` | `mvn spring-boot:run` | `3006` | blocking queue + background consumer thread |
| Dart | [`hello_dart`](./hello_dart/README.md) | `pubspec.yaml` | `bin/main.dart` | Dart process ที่รันผ่าน `dart run` | `dart run bin/main.dart` | `3007` | `StreamController` + async consumer |
| Bash | [`hello_bash`](./hello_bash/README.md) | ไม่มีไฟล์ dependency แยกในตัวอย่างนี้ | `server.sh` | Bash process ที่รันผ่าน `bash` | `bash server.sh` | `3008` | file queue + background loop |

## สรุปภาพรวมแบบ Event-Driven

ตอนนี้ทุกโปรเจกต์ใช้ flow เปรียบเทียบเดียวกัน:

1. client ส่ง HTTP request
2. route handler สร้าง JSON response
3. route handler publish event ภายในระบบ
4. consumer ทำงานต่อด้านหลัง
5. event ที่ถูก consume แล้วถูกเก็บใน `events/request-events.jsonl`

เป้าหมายหลักของชุดนี้คือการเปรียบเทียบแนวคิด ไม่ใช่การบังคับให้ทุกภาษาต้องใช้ implementation ที่เหมือนกันทุกบรรทัด

เพราะฉะนั้นแต่ละภาษาจึงใช้กลไก event ที่เหมาะกับ runtime ของตัวเองมากกว่า

## สถานะการตรวจจริง

| ภาษา | สถานะ |
| --- | --- |
| Rust | ตรวจ live request และ event log แล้ว |
| Go | ตรวจ live request และ event log แล้ว |
| Python | ตรวจ live request และ event log แล้ว |
| JavaScript | อัปเดตโค้ดและ README แล้ว แต่เครื่องนี้ยังไม่มี runtime |
| PHP | อัปเดตโค้ดและ README แล้ว แต่เครื่องนี้ยังไม่มี runtime |
| C# | อัปเดตโค้ดและ README แล้ว แต่เครื่องนี้ยังไม่มี runtime |
| Java | อัปเดตโค้ดและ README แล้ว มี `java` แต่ยังไม่มี `mvn` |
| Dart | อัปเดตโค้ดและ README แล้ว แต่เครื่องนี้ยังไม่มี runtime |
| Bash | ตรวจ syntax script ด้วย `bash -n` แล้ว |

## สถานะ Runtime ในเครื่องตอนนี้

สถานะที่ตรวจพบในเครื่องปัจจุบัน:

| เครื่องมือ | สถานะ |
| --- | --- |
| `cargo` | พร้อมใช้งาน |
| `go` | พร้อมใช้งาน |
| `python3` | พร้อมใช้งาน |
| `node` | ยังไม่พบ |
| `php` | ยังไม่พบ |
| `dotnet` | ยังไม่พบ |
| `java` | พร้อมใช้งาน |
| `dart` | ยังไม่พบ |
| `bash` | พร้อมใช้งาน |
| `mvn` | ยังไม่พบ |

## หมายเหตุ

- Rust, Go และ Python เป็นตัวอย่างที่สมบูรณ์ที่สุดตอนนี้ เพราะตรวจ event-driven flow แบบ end-to-end แล้ว
- Java มี runtime แล้ว แต่ยังไม่มี Maven ดังนั้นตัวอย่าง Spring Boot จึงพร้อมในระดับโค้ด แต่ยังไม่ได้รันจริงในเครื่องนี้
- JavaScript, PHP, C#, และ Dart มีโครง event-driven ครบแล้ว แต่ยังต้องติดตั้ง runtime เพิ่มก่อนถึงจะ verify ได้
- Bash ตั้งใจทำให้เรียบง่าย แต่ก็ยังแสดง producer, queue, consumer และ JSONL event output ได้ชัด

## เป้าหมายของโปรเจกต์นี้

เป้าหมายของชุดนี้ไม่ใช่แค่ทำ app เดียวกันหลายภาษา แต่เพื่อใช้เปรียบเทียบว่าแต่ละ ecosystem มองเรื่องเหล่านี้อย่างไร:
- ไฟล์ dependency
- โครงสร้าง source
- build output
- คำสั่ง run
- การจัด route ของ HTTP
- การออกแบบ JSON response
- การ publish event ภายใน
- การ consume event ด้านหลัง
- รูปแบบ event-driven ที่เหมาะกับ runtime ของแต่ละภาษา

## ลำดับการอ่านที่แนะนำ

ถ้าต้องการเรียนแบบค่อย ๆ เห็นภาพ ลำดับนี้กำลังดี:

1. Rust
2. Go
3. Python
4. JavaScript
5. PHP
6. C#
7. Java
8. Dart
9. Bash
