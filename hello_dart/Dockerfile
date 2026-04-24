# syntax=docker/dockerfile:1

FROM dart:stable AS builder

WORKDIR /app
COPY pubspec.yaml ./
COPY bin ./bin
RUN dart pub get

FROM dart:stable

RUN useradd -r -m -d /app appuser

WORKDIR /app

COPY --from=builder /app /app

RUN mkdir -p /app/events \
    && chown -R appuser:appuser /app

ENV APP_HOST=0.0.0.0
ENV PORT=3007

EXPOSE 3007

USER appuser

CMD ["dart", "run", "bin/main.dart"]
