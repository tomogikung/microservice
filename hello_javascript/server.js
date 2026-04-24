import express from "express";
import { randomUUID } from "node:crypto";
import { appendFile, mkdir } from "node:fs/promises";

const app = express();
const SERVICE_NAME = "hello_javascript";
const HOST = process.env.APP_HOST || "127.0.0.1";
const PORT = Number(process.env.PORT || "3003");
const EVENT_LOG_PATH = "events/request-events.jsonl";
const MAX_QUEUE_SIZE = 128;

const appState = {
  eventQueue: [],
  waitingConsumer: null,
};

app.locals.state = appState;

function requestInfo(req, traceId) {
  return {
    method: req.method,
    path: req.path,
    trace_id: traceId,
  };
}

function newTraceId() {
  return randomUUID();
}

function thailandTimeString(now) {
  return (
    new Intl.DateTimeFormat("sv-SE", {
      timeZone: "Asia/Bangkok",
      hour12: false,
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    })
      .format(now)
      .replace(" ", "T") + "+07:00"
  );
}

function buildEvent(req, eventType, traceId, responseMessage) {
  return {
    event_id: randomUUID(),
    event_type: eventType,
    emitted_at_utc: new Date().toISOString(),
    service: SERVICE_NAME,
    trace_id: traceId,
    request: requestInfo(req, traceId),
    data: {
      route: req.path,
      response_message: responseMessage,
      response_timestamp: Math.floor(Date.now() / 1000),
    },
  };
}

function publishEvent(state, req, eventType, traceId, responseMessage) {
  if (state.eventQueue.length >= MAX_QUEUE_SIZE) {
    return "dropped";
  }

  state.eventQueue.push(buildEvent(req, eventType, traceId, responseMessage));

  if (state.waitingConsumer) {
    state.waitingConsumer();
    state.waitingConsumer = null;
  }

  return "queued";
}

async function nextEvent(state) {
  if (state.eventQueue.length > 0) {
    return state.eventQueue.shift();
  }

  return new Promise((resolve) => {
    state.waitingConsumer = () => resolve(state.eventQueue.shift());
  });
}

async function eventConsumer(state) {
  await mkdir("events", { recursive: true });

  while (true) {
    const event = await nextEvent(state);
    await appendFile(EVENT_LOG_PATH, `${JSON.stringify(event)}\n`, "utf8");
  }
}

eventConsumer(appState).catch((error) => {
  console.error("Event consumer failed:", error);
});

app.get("/", (req, res) => {
  const traceId = newTraceId();
  const eventStatus = publishEvent(
    req.app.locals.state,
    req,
    "root_requested",
    traceId,
    "Welcome to hello_javascript API",
  );

  res.json({
    status: "success",
    trace_id: traceId,
    message: "Welcome to hello_javascript API",
    event_status: eventStatus,
    data: {
      service: SERVICE_NAME,
      version: "0.1.0",
      architecture: "request-response + event consumer",
      event_log_file: EVENT_LOG_PATH,
      available_routes: ["/", "/time", "/health"],
    },
    request: requestInfo(req, traceId),
  });
});

app.get("/time", (req, res) => {
  const traceId = newTraceId();
  const now = new Date();
  const eventStatus = publishEvent(
    req.app.locals.state,
    req,
    "time_requested",
    traceId,
    "Current server time",
  );

  res.json({
    status: "success",
    trace_id: traceId,
    message: "Current server time",
    event_status: eventStatus,
    data: {
      timestamp: Math.floor(now.getTime() / 1000),
      datetime_utc: now.toISOString(),
      datetime_th: thailandTimeString(now),
      timezone: "Asia/Bangkok",
      utc_offset: "+07:00",
    },
    request: requestInfo(req, traceId),
  });
});

app.get("/health", (req, res) => {
  const traceId = newTraceId();
  const eventStatus = publishEvent(
    req.app.locals.state,
    req,
    "health_requested",
    traceId,
    "Service is healthy",
  );

  res.json({
    status: "success",
    trace_id: traceId,
    message: "Service is healthy",
    event_status: eventStatus,
    data: {
      service: SERVICE_NAME,
      healthy: true,
      event_consumer: "async file logger",
    },
    request: requestInfo(req, traceId),
  });
});

app.listen(PORT, HOST, () => {
  console.log(`Server running at http://${HOST}:${PORT}`);
});
