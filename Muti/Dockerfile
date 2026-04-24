# syntax=docker/dockerfile:1

FROM rust:1.94-bookworm AS builder

WORKDIR /app
COPY Cargo.toml Cargo.lock* ./
COPY src ./src
RUN cargo build --locked --release

FROM debian:bookworm-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -r -m -d /app appuser

WORKDIR /app

COPY --from=builder /app/target/release/muti_axum /usr/local/bin/muti_axum

ENV APP_HOST=0.0.0.0
ENV PORT=3009

EXPOSE 3009

USER appuser

CMD ["muti_axum"]
