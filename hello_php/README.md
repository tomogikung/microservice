# hello_php

PHP API example using plain PHP routing.

Default port: `127.0.0.1:3004`

## Project Structure

- Dependency: `composer.json`
- Source: `public/index.php`
- Consumer: `consumer.php`
- Execute: PHP process started by the built-in server or web server
- Event queue: `events/pending/`
- Event log: `events/request-events.jsonl`
- Run: `php -S 127.0.0.1:3004 -t public`
- Consume events: `php consumer.php`

## What Each File Does

### `composer.json`

This is the dependency and project configuration file.

It defines:
- project name
- package type
- autoload settings
- external packages used by the project

In this project, `composer.json` is minimal because the API structure is written with plain PHP.

### `public/index.php`

This is the main source file of the project.

It contains:
- simple route matching
- JSON response helper
- request metadata helper
- event publishing into an outbox queue
- time and health responses

Current routes:
- `/` returns welcome information
- `/time` returns time data in UTC and Thailand time
- `/health` returns service health status

Current event behavior:
- every request publishes an event file into `events/pending/`
- events stay queued there until the consumer processes them

### `consumer.php`

This is the event consumer for the PHP project.

It contains:
- logic for reading queued event files from `events/pending/`
- appending those events into `events/request-events.jsonl`
- removing consumed event files after they are processed

### Execute

PHP does not create a compiled executable in this basic setup.

The app runs as a PHP process through:

```bash
php -S 127.0.0.1:3004 -t public
```

The event consumer runs as a separate PHP process:

```bash
php consumer.php
```

## Event-Driven Shape

This project now uses a simple event-driven pattern adapted for plain PHP.

The HTTP handler still responds to the client immediately, but it also publishes an event file into an outbox directory.

A separate consumer script then reads queued event files and writes them into the final JSONL event log.

Flow:

1. client sends request
2. route handler creates response data
3. route handler publishes an event file into `events/pending/`
4. `consumer.php` reads queued event files
5. consumed events are written to `events/request-events.jsonl`

This is not a full broker-based event-driven architecture yet, but it is a clear first step toward one and it fits the plain PHP runtime model.

## How `php -S 127.0.0.1:3004 -t public` Works

When you run:

```bash
php -S 127.0.0.1:3004 -t public
```

PHP works in this order:

1. Read project configuration from `composer.json`
2. Load source code from `public/index.php`
3. Start the built-in PHP server
4. Listen for requests on `127.0.0.1:3004`
5. Route each request through `index.php`

## Request Flow in This Project

When a browser or client calls:

```text
GET http://127.0.0.1:3004/time
```

the flow is:

1. PHP receives the request
2. `index.php` checks the path
3. The `/time` branch is selected
4. The code creates:
   - UTC time
   - Thailand time
   - `trace_id`
   - request metadata
5. The route publishes a `time_requested` event file into `events/pending/`
6. PHP converts the response into JSON
7. The API returns the JSON response to the client
8. `consumer.php` can then append that event into `events/request-events.jsonl`

## Run the Project

From the `hello_php` directory:

```bash
php -S 127.0.0.1:3004 -t public
```

Then open:

- `http://127.0.0.1:3004/`
- `http://127.0.0.1:3004/time`
- `http://127.0.0.1:3004/health`

After calling the API, run:

```bash
php consumer.php
```

Then inspect:

```text
events/request-events.jsonl
```

to see the consumed events.

## Summary

- `composer.json` tells PHP about the project setup
- `public/index.php` contains the application logic
- `consumer.php` drains queued events into the final log
- `events/pending/` stores queued event files
- `events/request-events.jsonl` stores consumed events
- `php -S ...` runs the API server
- this project uses port `3004`
