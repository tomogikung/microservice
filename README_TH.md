# ตัวอย่าง API หลายภาษา

repository นี้รวบรวมโปรเจกต์ API แนวคิดเดียวกันในหลายภาษา เพื่อให้เปรียบเทียบกันได้แบบตรง ๆ

แต่ละโปรเจกต์ใช้รูปแบบเดียวกัน:
- `GET /`
- `GET /time`
- `GET /health`
- response มี `status`, `trace_id`, `message`, `data`, `request`

## ตารางเปรียบเทียบ

| ภาษา | โปรเจกต์ | ไฟล์ Dependency | ไฟล์ Source | ไฟล์ Execute / Output | คำสั่ง Run | Port |
| --- | --- | --- | --- | --- | --- | --- |
| Rust | [`hello_rust`](./hello_rust/README) | `Cargo.toml` | `src/main.rs` | `target/debug/hello_rust` หรือ `target/release/hello_rust` | `cargo run` | `3000` |
| Go | [`hello_go`](./hello_go/README.md) | `go.mod` | `main.go` | binary ที่ build ออกมา เช่น `hello_go` | `go run .` | `3001` |
| Python | [`hello_python`](./hello_python/README.md) | `requirements.txt` | `main.py` | Python process ที่รันผ่าน `uvicorn` | `uvicorn main:app --reload --port 3002` | `3002` |
| JavaScript | [`hello_javascript`](./hello_javascript/README.md) | `package.json` | `server.js` | Node.js process ที่รันผ่าน `node` | `npm install && npm start` | `3003` |
| PHP | [`hello_php`](./hello_php/README.md) | `composer.json` | `public/index.php` | PHP process ที่รันผ่าน built-in server | `php -S 127.0.0.1:3004 -t public` | `3004` |
| C# | [`hello_csharp`](./hello_csharp/README.md) | `hello_csharp.csproj` | `Program.cs` | `bin/Debug/net8.0/hello_csharp` หรือ `bin/Release/net8.0/hello_csharp` | `dotnet run` | `3005` |
| Java | [`hello_java`](./hello_java/README.md) | `pom.xml` | `src/main/java/com/example/hello_java/` | `target/hello_java-0.1.0.jar` | `mvn spring-boot:run` | `3006` |
| Dart | [`hello_dart`](./hello_dart/README.md) | `pubspec.yaml` | `bin/main.dart` | Dart process ที่รันผ่าน `dart run` | `dart run bin/main.dart` | `3007` |
| Bash | [`hello_bash`](./hello_bash/README.md) | ไม่มีไฟล์ dependency แยกในตัวอย่างนี้ | `server.sh` | Bash process ที่รันผ่าน `bash` | `bash server.sh` | `3008` |

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

- Rust, Go และ Python เป็นกลุ่มที่พร้อมต่อยอดให้รันจริงได้ง่ายที่สุดในเครื่องนี้
- Java มี runtime แล้ว แต่ยังไม่มี Maven
- JavaScript, PHP, C#, และ Dart ตอนนี้ยังอยู่ในสถานะเป็นโครงสร้างอ้างอิง จนกว่าจะติดตั้ง runtime เพิ่ม
- Bash มีพร้อมอยู่แล้ว แต่ตัวอย่าง server ตั้งใจทำให้เรียบง่ายเพื่อใช้เปรียบเทียบแนวคิดมากกว่าใช้งานจริง

## เป้าหมายของโปรเจกต์นี้

เป้าหมายของชุดนี้ไม่ใช่แค่ทำ app เดียวกันหลายภาษา แต่เพื่อใช้เปรียบเทียบว่าแต่ละ ecosystem มองเรื่องเหล่านี้อย่างไร:
- ไฟล์ dependency
- โครงสร้าง source
- build output
- คำสั่ง run
- การจัด route ของ HTTP
- การออกแบบ JSON response

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

## ไฟล์ที่เกี่ยวข้อง

- อังกฤษ: [README.md](./README.md)
- ไทย: [README_TH.md](./README_TH.md)
