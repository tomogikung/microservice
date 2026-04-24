# syntax=docker/dockerfile:1

FROM maven:3.9.9-eclipse-temurin-17 AS builder

WORKDIR /app
COPY pom.xml ./
COPY src ./src
RUN mvn -q -DskipTests package

FROM eclipse-temurin:17-jre-jammy

RUN useradd -r -m -d /app appuser

WORKDIR /app

COPY --from=builder /app/target/hello_java-0.1.0.jar /app/hello_java.jar

RUN mkdir -p /app/events \
    && chown -R appuser:appuser /app

ENV APP_HOST=0.0.0.0
ENV PORT=3006

EXPOSE 3006

USER appuser

CMD ["java", "-jar", "/app/hello_java.jar"]
