# hello_go

Go API example using the standard `net/http` package.

## Project Structure

- Dependency: `go.mod`
- Source: `main.go`
- Execute: compiled binary such as `hello_go`
- Run: `go run .`

## What Each File Does

### `go.mod`

This is the dependency and module configuration file.

It defines:
- module name
- Go version

In this project, `go.mod` is simple because the API uses Go standard library packages such as:
- `net/http`
- `encoding/json`
- `time`
- `log`

### `main.go`

This is the main source file of the project.

It contains:
- API response structs
- request metadata struct
- handler functions for each route
- the `main()` function that starts the server

Current routes:
- `/` returns welcome information
- `/time` returns time data in UTC and Thailand time
- `/health` returns service health status

### Executable File

Go can run the project directly with:

```bash
go run .
```

It can also build a binary with:

```bash
go build
```

That binary is the executable file for the project.

## How `go run .` Works

When you run:

```bash
go run .
```

Go works in this order:

1. Read `go.mod`
2. Load the source code from `main.go`
3. Compile the project
4. Create a temporary executable
5. Run the executable

If you use:

```bash
go build
```

Go creates a reusable binary file in the project directory.

## Request Flow in This Project

When a browser or client calls:

```text
GET http://127.0.0.1:3001/time
```

the flow is:

1. `main()` starts the HTTP server
2. Go matches the path `/time`
3. `timeHandler()` is called
4. The handler creates:
   - UTC time
   - Thailand time
   - `trace_id`
   - request metadata
5. Go serializes the response struct into JSON
6. The API returns the JSON response to the client

## Run the Project

From the `hello_go` directory:

```bash
go run .
```

Then open:

- `http://127.0.0.1:3001/`
- `http://127.0.0.1:3001/time`
- `http://127.0.0.1:3001/health`

## Summary

- `go.mod` tells Go about the module
- `main.go` contains the application logic
- `go run .` compiles and runs the project
- `go build` creates the executable file
