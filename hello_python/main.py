import asyncio
import json
import os
from contextlib import asynccontextmanager, suppress
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, Request


SERVICE_NAME = "hello_python"
PORT = int(os.getenv("PORT", "3002"))
EVENT_LOG_PATH = Path("events/request-events.jsonl")
THAILAND_TZ = timezone(timedelta(hours=7), name="Asia/Bangkok")


def new_id() -> str:
    return str(uuid4())


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def request_info(request: Request, trace_id: str) -> dict[str, str]:
    return {
        "method": request.method,
        "path": request.url.path,
        "trace_id": trace_id,
    }


def build_event(
    request: Request,
    event_type: str,
    trace_id: str,
    response_message: str,
) -> dict[str, Any]:
    now_utc = utc_now()
    return {
        "event_id": new_id(),
        "event_type": event_type,
        "emitted_at_utc": now_utc.isoformat(),
        "service": SERVICE_NAME,
        "trace_id": trace_id,
        "request": request_info(request, trace_id),
        "data": {
            "route": request.url.path,
            "response_message": response_message,
            "response_timestamp": int(now_utc.timestamp()),
        },
    }


def append_event_log(event: dict[str, Any]) -> None:
    EVENT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with EVENT_LOG_PATH.open("a", encoding="utf-8") as event_log:
        json.dump(event, event_log, ensure_ascii=True)
        event_log.write("\n")


async def event_consumer(event_queue: asyncio.Queue[dict[str, Any]]) -> None:
    while True:
        event = await event_queue.get()
        try:
            await asyncio.to_thread(append_event_log, event)
        finally:
            event_queue.task_done()


def publish_event(
    request: Request,
    event_type: str,
    trace_id: str,
    response_message: str,
) -> str:
    event_queue: asyncio.Queue[dict[str, Any]] = request.app.state.event_queue
    event = build_event(request, event_type, trace_id, response_message)

    try:
        event_queue.put_nowait(event)
        return "queued"
    except asyncio.QueueFull:
        return "dropped"


@asynccontextmanager
async def lifespan(app: FastAPI):
    event_queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue(maxsize=128)
    app.state.event_queue = event_queue
    consumer_task = asyncio.create_task(event_consumer(event_queue))

    try:
        yield
    finally:
        consumer_task.cancel()
        with suppress(asyncio.CancelledError):
            await consumer_task


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root(request: Request) -> dict[str, Any]:
    trace_id = new_id()
    event_status = publish_event(
        request,
        "root_requested",
        trace_id,
        "Welcome to hello_python API",
    )

    return {
        "status": "success",
        "trace_id": trace_id,
        "message": "Welcome to hello_python API",
        "event_status": event_status,
        "data": {
            "service": SERVICE_NAME,
            "version": "0.1.0",
            "architecture": "request-response + event consumer",
            "event_log_file": str(EVENT_LOG_PATH),
            "available_routes": ["/", "/time", "/health"],
        },
        "request": request_info(request, trace_id),
    }


@app.get("/time")
async def time(request: Request) -> dict[str, Any]:
    trace_id = new_id()
    now_utc = utc_now()
    now_th = now_utc.astimezone(THAILAND_TZ)
    event_status = publish_event(
        request,
        "time_requested",
        trace_id,
        "Current server time",
    )

    return {
        "status": "success",
        "trace_id": trace_id,
        "message": "Current server time",
        "event_status": event_status,
        "data": {
            "timestamp": int(now_utc.timestamp()),
            "datetime_utc": now_utc.isoformat(),
            "datetime_th": now_th.isoformat(),
            "timezone": "Asia/Bangkok",
            "utc_offset": "+07:00",
        },
        "request": request_info(request, trace_id),
    }


@app.get("/health")
async def health(request: Request) -> dict[str, Any]:
    trace_id = new_id()
    event_status = publish_event(
        request,
        "health_requested",
        trace_id,
        "Service is healthy",
    )

    return {
        "status": "success",
        "trace_id": trace_id,
        "message": "Service is healthy",
        "event_status": event_status,
        "data": {
            "service": SERVICE_NAME,
            "healthy": True,
            "event_consumer": "async file logger",
            "port": PORT,
        },
        "request": request_info(request, trace_id),
    }
