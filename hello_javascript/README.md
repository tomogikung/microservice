# hello_javascript

JavaScript API example using `Express`.

Default port: `127.0.0.1:3003`

## Project Structure

- Dependency: `package.json`
- Source: `server.js`
- Execute: Node.js process started by `node`
- Event log: `events/request-events.jsonl`
- Run: `npm start`

## What Each File Does

### `package.json`

This is the dependency and project configuration file.

It defines:
- project name
- version
- runtime mode
- scripts
- external packages used by the project

In this project, `package.json` includes:
- `express` for the web API

### `server.js`

This is the main source file of the project.

It contains:
- Express app setup
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
- every request publishes an event into an internal queue
- a background consumer reads queued events
- consumed events are appended to `events/request-events.jsonl`

### Execute

JavaScript does not create a compiled executable in this basic setup.

The app runs as a Node.js process through:

```bash
node server.js
```

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

## How `npm start` Works

When you run:

```bash
npm start
```

JavaScript works in this order:

1. Read `package.json`
2. Load dependencies from `node_modules`
3. Load source code from `server.js`
4. Start the background event consumer
5. Start the Express server
6. Listen for requests on `127.0.0.1:3003`

## Request Flow in This Project

When a browser or client calls:

```text
GET http://127.0.0.1:3003/time
```

the flow is:

1. Node.js receives the request
2. Express matches the path `/time`
3. The route handler is called
4. The handler creates:
   - UTC time
   - Thailand time
   - `trace_id`
   - request metadata
5. The handler publishes a `time_requested` event into the internal queue
6. JavaScript converts the response into JSON
7. The API returns the JSON response to the client
8. the background consumer writes the event into `events/request-events.jsonl`

## Run the Project

From the `hello_javascript` directory:

```bash
npm install
npm start
```

Then open:

- `http://127.0.0.1:3003/`
- `http://127.0.0.1:3003/time`
- `http://127.0.0.1:3003/health`

After calling the API, you can inspect:

```text
events/request-events.jsonl
```

to see the emitted events.

## Summary

- `package.json` tells JavaScript what packages are needed
- `server.js` contains the application logic
- `events/request-events.jsonl` stores consumed events
- `npm start` runs the API server
- this project uses port `3003`
