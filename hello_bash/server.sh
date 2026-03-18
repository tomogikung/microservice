#!/usr/bin/env bash

PORT=3008

trace_id() {
  date -u +"%Y%m%dT%H%M%S%N"
}

utc_now() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

th_now() {
  TZ=Asia/Bangkok date +"%Y-%m-%dT%H:%M:%S%z" | sed 's/\(..\)$/:\1/'
}

json_response() {
  local body="$1"
  printf 'HTTP/1.1 200 OK\r\n'
  printf 'Content-Type: application/json\r\n'
  printf 'Content-Length: %s\r\n' "${#body}"
  printf '\r\n'
  printf '%s' "$body"
}

not_found_response() {
  local body="$1"
  printf 'HTTP/1.1 404 Not Found\r\n'
  printf 'Content-Type: application/json\r\n'
  printf 'Content-Length: %s\r\n' "${#body}"
  printf '\r\n'
  printf '%s' "$body"
}

while true; do
  nc -l 127.0.0.1 "$PORT" | {
    read -r method path protocol
    trace_id_value="$(trace_id)"
    utc_value="$(utc_now)"
    th_value="$(th_now)"
    timestamp_value="$(date -u +%s)"

    if [[ "$path" == "/" ]]; then
      body=$(cat <<EOF
{"status":"success","trace_id":"$trace_id_value","message":"Welcome to hello_bash API","data":{"service":"hello_bash","version":"0.1.0","available_routes":["/","/time","/health"]},"request":{"method":"$method","path":"$path","trace_id":"$trace_id_value"}}
EOF
)
      json_response "$body"
    elif [[ "$path" == "/time" ]]; then
      body=$(cat <<EOF
{"status":"success","trace_id":"$trace_id_value","message":"Current server time","data":{"timestamp":$timestamp_value,"datetime_utc":"$utc_value","datetime_th":"$th_value","timezone":"Asia/Bangkok","utc_offset":"+07:00"},"request":{"method":"$method","path":"$path","trace_id":"$trace_id_value"}}
EOF
)
      json_response "$body"
    elif [[ "$path" == "/health" ]]; then
      body=$(cat <<EOF
{"status":"success","trace_id":"$trace_id_value","message":"Service is healthy","data":{"service":"hello_bash","healthy":true},"request":{"method":"$method","path":"$path","trace_id":"$trace_id_value"}}
EOF
)
      json_response "$body"
    else
      body=$(cat <<EOF
{"status":"error","trace_id":"$trace_id_value","message":"Route not found","data":null,"request":{"method":"$method","path":"$path","trace_id":"$trace_id_value"}}
EOF
)
      not_found_response "$body"
    fi
  }
done
