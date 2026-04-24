#!/usr/bin/env bash

SERVICE_NAME="hello_bash"
HOST="${APP_HOST:-127.0.0.1}"
PORT="${PORT:-3008}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EVENT_QUEUE_DIR="$SCRIPT_DIR/events/pending"
EVENT_LOG_PATH="$SCRIPT_DIR/events/request-events.jsonl"
EVENT_QUEUE_REL="events/pending"
EVENT_LOG_REL="events/request-events.jsonl"
CONSUMER_POLL_SECONDS=1

trace_id() {
  date -u +"%Y%m%dT%H%M%S%N"
}

utc_now() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

th_now() {
  TZ=Asia/Bangkok date +"%Y-%m-%dT%H:%M:%S%z" | sed 's/\(..\)$/:\1/'
}

json_escape() {
  local value="$1"
  value="${value//\\/\\\\}"
  value="${value//\"/\\\"}"
  value="${value//$'\r'/\\r}"
  value="${value//$'\n'/\\n}"
  value="${value//$'\t'/\\t}"
  printf '%s' "$value"
}

publish_event() {
  local method="$1"
  local path="$2"
  local trace_id_value="$3"
  local event_type="$4"
  local response_message="$5"
  local event_id event_file response_timestamp event_json method_json path_json response_message_json

  mkdir -p "$EVENT_QUEUE_DIR" || {
    printf 'dropped'
    return
  }

  event_id="$(trace_id)"
  response_timestamp="$(date -u +%s)"
  event_file="$EVENT_QUEUE_DIR/$event_id.json"
  method_json="$(json_escape "$method")"
  path_json="$(json_escape "$path")"
  response_message_json="$(json_escape "$response_message")"
  event_json=$(cat <<EOF
{"event_id":"$event_id","event_type":"$event_type","emitted_at_utc":"$(utc_now)","service":"$SERVICE_NAME","trace_id":"$trace_id_value","request":{"method":"$method_json","path":"$path_json","trace_id":"$trace_id_value"},"data":{"route":"$path_json","response_message":"$response_message_json","response_timestamp":$response_timestamp}}
EOF
)

  if printf '%s\n' "$event_json" > "$event_file"; then
    printf 'queued'
  else
    printf 'dropped'
  fi
}

event_consumer_loop() {
  mkdir -p "$EVENT_QUEUE_DIR"
  mkdir -p "$(dirname "$EVENT_LOG_PATH")"

  while true; do
    local processed=0
    local event_file

    shopt -s nullglob
    for event_file in "$EVENT_QUEUE_DIR"/*.json; do
      if [[ -s "$event_file" ]]; then
        cat "$event_file" >> "$EVENT_LOG_PATH"
        printf '\n' >> "$EVENT_LOG_PATH"
      fi
      rm -f "$event_file"
      processed=1
    done
    shopt -u nullglob

    if [[ "$processed" -eq 0 ]]; then
      sleep "$CONSUMER_POLL_SECONDS"
    fi
  done
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

event_consumer_loop &
consumer_pid=$!

cleanup() {
  kill "$consumer_pid" >/dev/null 2>&1 || true
}

trap cleanup EXIT INT TERM

printf 'Server running at http://%s:%s\n' "$HOST" "$PORT"

while true; do
  nc -l "$HOST" "$PORT" | {
    read -r method path protocol
    trace_id_value="$(trace_id)"
    method_json="$(json_escape "$method")"
    path_json="$(json_escape "$path")"
    utc_value="$(utc_now)"
    th_value="$(th_now)"
    timestamp_value="$(date -u +%s)"
    event_status=""

    if [[ "$path" == "/" ]]; then
      event_status="$(publish_event "$method" "$path" "$trace_id_value" "root_requested" "Welcome to hello_bash API")"
      body=$(cat <<EOF
{"status":"success","trace_id":"$trace_id_value","message":"Welcome to hello_bash API","event_status":"$event_status","data":{"service":"$SERVICE_NAME","version":"0.1.0","architecture":"request-response + event consumer","event_queue_dir":"$EVENT_QUEUE_REL","event_log_file":"$EVENT_LOG_REL","available_routes":["/","/time","/health"]},"request":{"method":"$method_json","path":"$path_json","trace_id":"$trace_id_value"}}
EOF
)
      json_response "$body"
    elif [[ "$path" == "/time" ]]; then
      event_status="$(publish_event "$method" "$path" "$trace_id_value" "time_requested" "Current server time")"
      body=$(cat <<EOF
{"status":"success","trace_id":"$trace_id_value","message":"Current server time","event_status":"$event_status","data":{"timestamp":$timestamp_value,"datetime_utc":"$utc_value","datetime_th":"$th_value","timezone":"Asia/Bangkok","utc_offset":"+07:00"},"request":{"method":"$method_json","path":"$path_json","trace_id":"$trace_id_value"}}
EOF
)
      json_response "$body"
    elif [[ "$path" == "/health" ]]; then
      event_status="$(publish_event "$method" "$path" "$trace_id_value" "health_requested" "Service is healthy")"
      body=$(cat <<EOF
{"status":"success","trace_id":"$trace_id_value","message":"Service is healthy","event_status":"$event_status","data":{"service":"$SERVICE_NAME","healthy":true,"event_consumer":"background file queue processor","port":$PORT},"request":{"method":"$method_json","path":"$path_json","trace_id":"$trace_id_value"}}
EOF
)
      json_response "$body"
    else
      event_status="$(publish_event "$method" "$path" "$trace_id_value" "route_not_found" "Route not found")"
      body=$(cat <<EOF
{"status":"error","trace_id":"$trace_id_value","message":"Route not found","event_status":"$event_status","data":null,"request":{"method":"$method_json","path":"$path_json","trace_id":"$trace_id_value"}}
EOF
)
      not_found_response "$body"
    fi
  }
done
