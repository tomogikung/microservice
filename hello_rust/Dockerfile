# syntax=docker/dockerfile:1

FROM rust:1.94-bookworm AS builder

WORKDIR /app
COPY Cargo.toml Cargo.lock ./
COPY src ./src
RUN cargo build --locked --release

FROM debian:bookworm-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -r -m -d /app appuser

WORKDIR /app

COPY --from=builder /app/target/release/hello_rust /usr/local/bin/hello_rust

RUN mkdir -p /app/events \
    && chown -R appuser:appuser /app

ENV APP_HOST=0.0.0.0
ENV PORT=3000

EXPOSE 3000

USER appuser

CMD ["hello_rust"]
