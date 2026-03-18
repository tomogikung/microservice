from datetime import datetime, timezone, timedelta
from uuid import uuid4

from fastapi import FastAPI, Request


app = FastAPI()
THAILAND_TZ = timezone(timedelta(hours=7), name="Asia/Bangkok")


def request_info(request: Request, trace_id: str) -> dict:
    return {
        "method": request.method,
        "path": request.url.path,
        "trace_id": trace_id,
    }


@app.get("/")
async def root(request: Request) -> dict:
    trace_id = str(uuid4())
    return {
        "status": "success",
        "trace_id": trace_id,
        "message": "Welcome to hello_python API",
        "data": {
            "service": "hello_python",
            "version": "0.1.0",
            "available_routes": ["/", "/time", "/health"],
        },
        "request": request_info(request, trace_id),
    }


@app.get("/time")
async def time(request: Request) -> dict:
    trace_id = str(uuid4())
    now_utc = datetime.now(timezone.utc)
    now_th = now_utc.astimezone(THAILAND_TZ)

    return {
        "status": "success",
        "trace_id": trace_id,
        "message": "Current server time",
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
async def health(request: Request) -> dict:
    trace_id = str(uuid4())
    return {
        "status": "success",
        "trace_id": trace_id,
        "message": "Service is healthy",
        "data": {
            "service": "hello_python",
            "healthy": True,
        },
        "request": request_info(request, trace_id),
    }
