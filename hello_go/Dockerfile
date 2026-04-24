# syntax=docker/dockerfile:1

FROM golang:1.22-bookworm AS builder

WORKDIR /app
COPY go.mod ./
COPY main.go ./
RUN CGO_ENABLED=0 GOOS=linux go build -o hello_go .

FROM debian:bookworm-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -r -m -d /app appuser

WORKDIR /app

COPY --from=builder /app/hello_go /usr/local/bin/hello_go

ENV APP_HOST=0.0.0.0
ENV PORT=3001

EXPOSE 3001

USER appuser

CMD ["hello_go"]
