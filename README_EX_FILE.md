# คู่มือการใช้งาน `ex_file` ในโปรเจกต์ microservice

ไฟล์ `ex_file` ในโปรเจกต์นี้ใช้เป็นเอกสารประกอบการเรียนรู้ Docker image ของแต่ละ microservice โดยสรุปว่า service นั้นควรมี `Dockerfile` แบบไหน ใช้คำสั่ง build อะไร ต้องมีไฟล์อะไรใน build context และตอนรันจริง container จะมีโครงสร้างประมาณใด

ไฟล์นี้ไม่ได้เป็นสคริปต์สำหรับรันโดยตรง แต่เป็น reference สำหรับอ่าน เปรียบเทียบ และนำไปสร้างหรือทบทวน `Dockerfile`

## ตำแหน่งไฟล์

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

## โครงสร้างเนื้อหาใน `ex_file`

แต่ละไฟล์มักแบ่งเป็นหัวข้อประมาณนี้:

| หัวข้อ | ความหมาย |
| --- | --- |
| `1. Real World` | ตัวอย่าง Dockerfile ที่ควรใช้จริง |
| `2. Command` | คำสั่งสำหรับ build Docker image |
| `3. Context` | ไฟล์หรือโฟลเดอร์ที่ต้องอยู่ใน build context |
| `4. Build stage` | รายละเอียด stage ที่ใช้ build หรือเตรียม dependency |
| `5. Runtime stage` | รายละเอียด image สุดท้ายที่ใช้ตอนรันจริง |
| `6. Real World line by line` | คำอธิบาย Dockerfile ทีละบรรทัด บาง service มีหัวข้อนี้ |

## วิธีใช้งานพื้นฐาน

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

## วิธีรัน container หลัง build

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

## การอ่าน Build stage และ Runtime stage

หลาย service ใช้ multi-stage build:

1. `Build stage` ใช้ image ที่มี compiler หรือ SDK เช่น `rust`, `golang`, `maven`, `dotnet/sdk`
2. `Runtime stage` ใช้ image ที่เล็กกว่า เช่น `debian:bookworm-slim`, `aspnet`, `jre`
3. ไฟล์ที่ build เสร็จแล้วจะถูก copy จาก build stage ไป runtime stage ด้วย `COPY --from=builder`

แนวคิดนี้ช่วยให้ image สุดท้ายเล็กลง และไม่ต้องมีเครื่องมือ build อยู่ใน container ตอน production

## การใช้งานกับ event log

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

## แนวทางเมื่อเพิ่ม service ใหม่

ถ้าจะเพิ่ม microservice ภาษาใหม่ ให้ทำตามรูปแบบนี้:

1. สร้างโฟลเดอร์ใหม่ เช่น `hello_newlang`
2. ใส่ source code หลักและไฟล์ dependency ของภาษานั้น
3. สร้าง `Dockerfile`
4. สร้าง `ex_file` เพื่ออธิบาย Dockerfile ตามหัวข้อเดียวกับ service อื่น
5. ระบุ command build, context, build stage, runtime stage และคำอธิบาย line by line
6. อัปเดต `README.md` และ `README_TH.md` ถ้าต้องการให้ service แสดงในตารางรวม

## ข้อควรระวัง

- ต้องรัน `docker build` จากโฟลเดอร์ของ service นั้น เพราะ build context จะอ้างอิงไฟล์ในโฟลเดอร์ปัจจุบัน
- ถ้า Dockerfile ใช้ `COPY` ไฟล์ใด ไฟล์นั้นต้องอยู่ใน build context จริง
- port ใน `docker run -p host:container` ควรตรงกับ `ENV PORT` และ `EXPOSE` ของ service
- service ที่เขียน event log ต้องมี permission เขียนไฟล์ใน `/app/events`
- ถ้าใช้ multi-stage build ชื่อไฟล์ output ต้องตรงกับไฟล์ที่ `COPY --from=builder` อ้างถึง
