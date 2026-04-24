# syntax=docker/dockerfile:1

FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim

RUN useradd -r -m -d /app appuser

WORKDIR /app

COPY --from=builder /install /usr/local
COPY main.py ./
COPY requirements.txt ./

ENV APP_HOST=0.0.0.0
ENV PORT=3002

EXPOSE 3002

USER appuser

CMD ["sh", "-c", "uvicorn main:app --host ${APP_HOST} --port ${PORT}"]
