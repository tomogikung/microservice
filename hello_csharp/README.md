# hello_csharp

C# API example using ASP.NET Core minimal API.

Default port: `127.0.0.1:3005`

## Project Structure

- Dependency: `hello_csharp.csproj`
- Source: `Program.cs`
- Execute: `bin/Debug/net8.0/hello_csharp` or `bin/Release/net8.0/hello_csharp`
- Event log: `events/request-events.jsonl`
- Run: `dotnet run`

## What Each File Does

### `hello_csharp.csproj`

This is the dependency and project configuration file.

It defines:
- project SDK
- target framework
- nullable settings
- implicit using behavior

In this project, the web API uses the ASP.NET Core web SDK through the project file.

### `Program.cs`

This is the main source file of the project.

It contains:
- ASP.NET Core app setup
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
- every request publishes an event into an internal `Channel<AppEvent>`
- a background hosted service consumes queued events
- consumed events are appended to `events/request-events.jsonl`

### Execute

When the project is built, .NET creates the application output under:

- `bin/Debug/net8.0/`
- `bin/Release/net8.0/`

## Event-Driven Shape

This project now uses a simple event-driven pattern inside the service.

The HTTP handler still responds to the client immediately, but it also publishes an internal event.

That event is then consumed by a background worker.

Flow:

1. client sends request
2. route handler creates response data
3. route handler publishes an event into an internal channel
4. background consumer receives the event
5. event is written to `events/request-events.jsonl`

This is not a full broker-based event-driven architecture yet, but it is a clear first step toward one.

## How `dotnet run` Works

When you run:

```bash
dotnet run
```

.NET works in this order:

1. Read `hello_csharp.csproj`
2. Resolve project dependencies
3. Load source code from `Program.cs`
4. Start the background event consumer
5. Compile the project
6. Create the application output in `bin/Debug/net8.0/`
7. Run the application

## Request Flow in This Project

When a browser or client calls:

```text
GET http://127.0.0.1:3005/time
```

the flow is:

1. ASP.NET Core receives the request
2. The route `/time` is matched
3. The handler creates:
   - UTC time
   - Thailand time
   - `trace_id`
   - request metadata
4. The handler publishes a `time_requested` event into the internal channel
5. C# converts the response into JSON
6. The API returns the JSON response to the client
7. the background consumer writes the event into `events/request-events.jsonl`

## Run the Project

From the `hello_csharp` directory:

```bash
dotnet run
```

Then open:

- `http://127.0.0.1:3005/`
- `http://127.0.0.1:3005/time`
- `http://127.0.0.1:3005/health`

After calling the API, you can inspect:

```text
events/request-events.jsonl
```

to see the emitted events.

## Summary

- `hello_csharp.csproj` tells .NET how the project is configured
- `Program.cs` contains the application logic
- `events/request-events.jsonl` stores consumed events
- `dotnet run` builds and runs the project
- this project uses port `3005`
