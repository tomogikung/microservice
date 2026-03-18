# hello_javascript

JavaScript API example using `Express`.

## Project Structure

- Dependency: `package.json`
- Source: `server.js`
- Execute: Node.js process started by `node`
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
- time and health responses

Current routes:
- `/` returns welcome information
- `/time` returns time data in UTC and Thailand time
- `/health` returns service health status

### Execute

JavaScript does not create a compiled executable in this basic setup.

The app runs as a Node.js process through:

```bash
node server.js
```

## How `npm start` Works

When you run:

```bash
npm start
```

JavaScript works in this order:

1. Read `package.json`
2. Load dependencies from `node_modules`
3. Load source code from `server.js`
4. Start the Express server
5. Listen for requests on `127.0.0.1:3003`

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
5. JavaScript converts the response into JSON
6. The API returns the JSON response to the client

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

## Summary

- `package.json` tells JavaScript what packages are needed
- `server.js` contains the application logic
- `npm start` runs the API server
- this project uses port `3003`
