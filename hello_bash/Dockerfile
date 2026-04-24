# syntax=docker/dockerfile:1

FROM debian:bookworm-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash netcat-openbsd coreutils sed tzdata \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -r -m -d /app appuser

WORKDIR /app

COPY server.sh ./

RUN chmod +x /app/server.sh \
    && mkdir -p /app/events/pending \
    && chown -R appuser:appuser /app

ENV APP_HOST=0.0.0.0
ENV PORT=3008

EXPOSE 3008

USER appuser

CMD ["bash", "server.sh"]
