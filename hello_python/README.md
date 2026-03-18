# hello_python

Python API example using `FastAPI`.

## Project Structure

- Dependency: `requirements.txt`
- Source: `main.py`
- Execute: Python process started by `uvicorn`
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
- FastAPI app setup
- route handlers
- request metadata helper
- time and health responses

Current routes:
- `/` returns welcome information
- `/time` returns time data in UTC and Thailand time
- `/health` returns service health status

### Execute

Python does not create a compiled executable in this basic setup.

The app runs as a Python process through `uvicorn`.

## How `uvicorn main:app --reload --port 3002` Works

When you run:

```bash
uvicorn main:app --reload --port 3002
```

Python works in this order:

1. Read dependencies from `requirements.txt`
2. Load source code from `main.py`
3. Import the `app` object
4. Start the FastAPI server with Uvicorn
5. Listen for requests on `127.0.0.1:3002`

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
5. Python converts the response into JSON
6. The API returns the JSON response to the client

## Run the Project

From the `hello_python` directory:

```bash
uvicorn main:app --reload --port 3002
```

Then open:

- `http://127.0.0.1:3002/`
- `http://127.0.0.1:3002/time`
- `http://127.0.0.1:3002/health`

## Summary

- `requirements.txt` tells Python what packages are needed
- `main.py` contains the application logic
- `uvicorn` runs the API server
- this project uses port `3002`
