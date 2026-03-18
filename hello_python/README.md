# hello_python

Python API example using `FastAPI`.

Default port: `127.0.0.1:3002`

## Project Structure

- Dependency: `requirements.txt`
- Source: `main.py`
- Execute: Python process started by `uvicorn`
- Event log: `events/request-events.jsonl`
- Run: `uvicorn main:app --reload --port 3002`

## What Each File Does

### `requirements.txt`

This is the dependency file for the Python project.

It defines the packages used by the API:
- `fastapi`
- `uvicorn`

### `main.py`

This is the main source file of the project.

It contains:
- FastAPI app setup with lifespan state
- route handlers
- request metadata helper
- internal event publishing
- background event consumer
- time and health responses

Current routes:
- `/` returns welcome information
- `/time` returns time data in UTC and Thailand time
- `/health` returns service health status

Current event behavior:
- every request publishes an event into an internal `asyncio.Queue`
- a background consumer reads the queued events
- consumed events are appended to `events/request-events.jsonl`

### Execute

Python does not create a compiled executable in this basic setup.

The app runs as a Python process through `uvicorn`.

## Event-Driven Shape

This project now uses a simple event-driven pattern inside the service.

The HTTP handler still responds to the client immediately, but it also publishes an internal event.

That event is then consumed by a background worker.

Flow:

1. client sends request
2. route handler creates response data
3. route handler publishes an event into an internal queue
4. background consumer receives the event
5. event is written to `events/request-events.jsonl`

This is not a full broker-based event-driven architecture yet, but it is a clear first step toward one.

## How `uvicorn main:app --reload --port 3002` Works

When you run:

```bash
uvicorn main:app --reload --port 3002
```

Python works in this order:

1. Read dependencies from `requirements.txt`
2. Load source code from `main.py`
3. Import the `app` object
4. Create shared state through the FastAPI lifespan hook
5. Start the background event consumer
6. Start the FastAPI server with Uvicorn
7. Listen for requests on `127.0.0.1:3002`

## Request Flow in This Project

When a browser or client calls:

```text
GET http://127.0.0.1:3002/time
```

the flow is:

1. Uvicorn receives the request
2. FastAPI matches the path `/time`
3. The `time()` handler is called
4. The handler creates:
   - UTC time
   - Thailand time
   - `trace_id`
   - request metadata
5. The handler publishes a `time_requested` event into the internal queue
6. Python converts the response into JSON
7. The API returns the JSON response to the client
8. the background consumer writes the event into `events/request-events.jsonl`

## Run the Project

From the `hello_python` directory:

```bash
uvicorn main:app --reload --port 3002
```

Then open:

- `http://127.0.0.1:3002/`
- `http://127.0.0.1:3002/time`
- `http://127.0.0.1:3002/health`

After calling the API, you can inspect:

```text
events/request-events.jsonl
```

to see the emitted events.

## Summary

- `requirements.txt` tells Python what packages are needed
- `main.py` contains the application logic
- `events/request-events.jsonl` stores consumed events
- `uvicorn` runs the API server
- this project uses port `3002`
