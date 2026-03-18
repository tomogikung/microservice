import express from "express";
import { randomUUID } from "node:crypto";

const app = express();
const PORT = 3003;

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

app.get("/", (req, res) => {
  const traceId = newTraceId();

  res.json({
    status: "success",
    trace_id: traceId,
    message: "Welcome to hello_javascript API",
    data: {
      service: "hello_javascript",
      version: "0.1.0",
      available_routes: ["/", "/time", "/health"],
    },
    request: requestInfo(req, traceId),
  });
});

app.get("/time", (req, res) => {
  const traceId = newTraceId();
  const now = new Date();
  const thailandTime = new Intl.DateTimeFormat("sv-SE", {
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
    .replace(" ", "T") + "+07:00";

  res.json({
    status: "success",
    trace_id: traceId,
    message: "Current server time",
    data: {
      timestamp: Math.floor(now.getTime() / 1000),
      datetime_utc: now.toISOString(),
      datetime_th: thailandTime,
      timezone: "Asia/Bangkok",
      utc_offset: "+07:00",
    },
    request: requestInfo(req, traceId),
  });
});

app.get("/health", (req, res) => {
  const traceId = newTraceId();

  res.json({
    status: "success",
    trace_id: traceId,
    message: "Service is healthy",
    data: {
      service: "hello_javascript",
      healthy: true,
    },
    request: requestInfo(req, traceId),
  });
});

app.listen(PORT, "127.0.0.1", () => {
  console.log(`Server running at http://127.0.0.1:${PORT}`);
});
