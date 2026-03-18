# hello_csharp

C# API example using ASP.NET Core minimal API.

## Project Structure

- Dependency: `hello_csharp.csproj`
- Source: `Program.cs`
- Execute: `bin/Debug/net8.0/hello_csharp` or `bin/Release/net8.0/hello_csharp`
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
- time and health responses

Current routes:
- `/` returns welcome information
- `/time` returns time data in UTC and Thailand time
- `/health` returns service health status

### Execute

When the project is built, .NET creates the application output under:

- `bin/Debug/net8.0/`
- `bin/Release/net8.0/`

## How `dotnet run` Works

When you run:

```bash
dotnet run
```

.NET works in this order:

1. Read `hello_csharp.csproj`
2. Resolve project dependencies
3. Load source code from `Program.cs`
4. Compile the project
5. Create the application output in `bin/Debug/net8.0/`
6. Run the application

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
4. C# converts the response into JSON
5. The API returns the JSON response to the client

## Run the Project

From the `hello_csharp` directory:

```bash
dotnet run
```

Then open:

- `http://127.0.0.1:3005/`
- `http://127.0.0.1:3005/time`
- `http://127.0.0.1:3005/health`

## Summary

- `hello_csharp.csproj` tells .NET how the project is configured
- `Program.cs` contains the application logic
- `dotnet run` builds and runs the project
- this project uses port `3005`
