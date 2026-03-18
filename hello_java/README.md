# hello_java

Java API example using Spring Boot.

## Project Structure

- Dependency: `pom.xml`
- Source: `src/main/java/com/example/hello_java/`
- Execute: `target/hello_java-0.1.0.jar`
- Run: `mvn spring-boot:run`

## What Each File Does

### `pom.xml`

This is the dependency and project configuration file.

It defines:
- project coordinates
- Java version
- build plugins
- external packages used by the project

In this project, `pom.xml` includes:
- `spring-boot-starter-web` for the web API

### `src/main/java/com/example/hello_java/HelloJavaApplication.java`

This is the application entry point.

It starts the Spring Boot application.

### `src/main/java/com/example/hello_java/ApiController.java`

This is the main API source file.

It contains:
- route handlers
- request metadata helper
- time and health responses

Current routes:
- `/` returns welcome information
- `/time` returns time data in UTC and Thailand time
- `/health` returns service health status

### `src/main/resources/application.properties`

This file contains application configuration.

In this project, it sets:
- `server.port=3006`

### Execute

When the project is built, Maven creates output under `target/`.

The runnable package is typically:

- `target/hello_java-0.1.0.jar`

## How `mvn spring-boot:run` Works

When you run:

```bash
mvn spring-boot:run
```

Java works in this order:

1. Read `pom.xml`
2. Resolve dependencies
3. Load source code from `src/main/java/...`
4. Compile the project
5. Start the Spring Boot application
6. Listen for requests on `127.0.0.1:3006`

## Request Flow in This Project

When a browser or client calls:

```text
GET http://127.0.0.1:3006/time
```

the flow is:

1. Spring Boot receives the request
2. The route `/time` is matched
3. The `time()` handler is called
4. The handler creates:
   - UTC time
   - Thailand time
   - `trace_id`
   - request metadata
5. Java converts the response into JSON
6. The API returns the JSON response to the client

## Run the Project

From the `hello_java` directory:

```bash
mvn spring-boot:run
```

Then open:

- `http://127.0.0.1:3006/`
- `http://127.0.0.1:3006/time`
- `http://127.0.0.1:3006/health`

## Summary

- `pom.xml` tells Java how the project is configured
- `src/main/java/...` contains the application logic
- `target/` contains the build output
- `mvn spring-boot:run` builds and runs the project
- this project uses port `3006`
