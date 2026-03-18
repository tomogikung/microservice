# hello_php

PHP API example using plain PHP routing.

## Project Structure

- Dependency: `composer.json`
- Source: `public/index.php`
- Execute: PHP process started by the built-in server or web server
- Run: `php -S 127.0.0.1:3004 -t public`

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
- time and health responses

Current routes:
- `/` returns welcome information
- `/time` returns time data in UTC and Thailand time
- `/health` returns service health status

### Execute

PHP does not create a compiled executable in this basic setup.

The app runs as a PHP process through:

```bash
php -S 127.0.0.1:3004 -t public
```

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
5. PHP converts the response into JSON
6. The API returns the JSON response to the client

## Run the Project

From the `hello_php` directory:

```bash
php -S 127.0.0.1:3004 -t public
```

Then open:

- `http://127.0.0.1:3004/`
- `http://127.0.0.1:3004/time`
- `http://127.0.0.1:3004/health`

## Summary

- `composer.json` tells PHP about the project setup
- `public/index.php` contains the application logic
- `php -S ...` runs the API server
- this project uses port `3004`
