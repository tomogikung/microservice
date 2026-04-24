# syntax=docker/dockerfile:1

FROM php:8.3-cli-bookworm

RUN useradd -r -m -d /app appuser

WORKDIR /app

COPY composer.json ./
COPY consumer.php ./
COPY public ./public

RUN mkdir -p /app/events/pending \
    && chown -R appuser:appuser /app

ENV APP_HOST=0.0.0.0
ENV PORT=3004

EXPOSE 3004

USER appuser

CMD ["sh", "-c", "while true; do php consumer.php; sleep 1; done & exec php -S ${APP_HOST}:${PORT} -t public"]
