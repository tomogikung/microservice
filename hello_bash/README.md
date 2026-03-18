# hello_bash

Bash API example using a simple shell script server.

Default port: `127.0.0.1:3008`

## Project Structure

- Dependency: no package dependency file in this basic setup
- Source: `server.sh`
- Execute: Bash process started by `bash`
- Event queue: `events/pending/`
- Event log: `events/request-events.jsonl`
- Run: `bash server.sh`

## What Each File Does

### `server.sh`

This is the main source file of the project.

It contains:
- a simple loop-based server
- JSON response helpers
- request metadata helper
- event publishing into queued files
- background event consumer loop
- time and health responses

Current routes:
- `/` returns welcome information
- `/time` returns time data in UTC and Thailand time
- `/health` returns service health status

Current event behavior:
- every request publishes an event file into `events/pending/`
- a background Bash loop consumes queued events
- consumed events are appended to `events/request-events.jsonl`

### Execute

Bash does not create a compiled executable in this setup.

The app runs directly as a shell process through:

```bash
bash server.sh
```

## Event-Driven Shape

This project now uses a simple event-driven pattern adapted for Bash.

The request handler still responds to the client immediately, but it also publishes an event file into a queue directory.

A background consumer loop then reads queued event files and writes them into the final JSONL event log.

Flow:

1. client sends request
2. route handler creates response data
3. route handler publishes an event file into `events/pending/`
4. background consumer loop reads queued event files
5. consumed events are written to `events/request-events.jsonl`

This is not a full broker-based event-driven architecture yet, but it is a clear first step toward one and it fits a Bash-only setup.

## How `bash server.sh` Works

When you run:

```bash
bash server.sh
```

Bash works in this order:

1. Load the shell script from `server.sh`
2. Start the background event consumer loop
3. Start a simple listener loop
4. Wait for a request on `127.0.0.1:3008`
5. Build a JSON response from shell commands
6. Return the response to the client

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
5. The route publishes a `time_requested` event file into `events/pending/`
6. Bash prints the JSON response
7. The API returns the JSON response to the client
8. the background consumer appends the event into `events/request-events.jsonl`

## Run the Project

From the `hello_bash` directory:

```bash
bash server.sh
```

Then open:

- `http://127.0.0.1:3008/`
- `http://127.0.0.1:3008/time`
- `http://127.0.0.1:3008/health`

After calling the API, you can inspect:

```text
events/request-events.jsonl
```

to see the consumed events.

## Summary

- Bash has no dependency file in this simple version
- `server.sh` contains the application logic
- `events/pending/` stores queued event files
- `events/request-events.jsonl` stores consumed events
- `bash server.sh` runs the API server
- this project uses port `3008`
