# hello_bash

Bash API example using a simple shell script server.

## Project Structure

- Dependency: no package dependency file in this basic setup
- Source: `server.sh`
- Execute: Bash process started by `bash`
- Run: `bash server.sh`

## What Each File Does

### `server.sh`

This is the main source file of the project.

It contains:
- a simple loop-based server
- JSON response helpers
- request metadata helper
- time and health responses

Current routes:
- `/` returns welcome information
- `/time` returns time data in UTC and Thailand time
- `/health` returns service health status

### Execute

Bash does not create a compiled executable in this setup.

The app runs directly as a shell process through:

```bash
bash server.sh
```

## How `bash server.sh` Works

When you run:

```bash
bash server.sh
```

Bash works in this order:

1. Load the shell script from `server.sh`
2. Start a simple listener loop
3. Wait for a request on `127.0.0.1:3008`
4. Build a JSON response from shell commands
5. Return the response to the client

## Request Flow in This Project

When a browser or client calls:

```text
GET http://127.0.0.1:3008/time
```

the flow is:

1. The shell script receives the request through `nc`
2. Bash reads the method and path
3. The `/time` branch is selected
4. The script creates:
   - UTC time
   - Thailand time
   - `trace_id`
   - request metadata
5. Bash prints the JSON response
6. The API returns the JSON response to the client

## Run the Project

From the `hello_bash` directory:

```bash
bash server.sh
```

Then open:

- `http://127.0.0.1:3008/`
- `http://127.0.0.1:3008/time`
- `http://127.0.0.1:3008/health`

## Summary

- Bash has no dependency file in this simple version
- `server.sh` contains the application logic
- `bash server.sh` runs the API server
- this project uses port `3008`
