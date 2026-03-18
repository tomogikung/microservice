package com.example.hello_java;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.Instant;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@RestController
public class ApiController {

    private Map<String, Object> requestInfo(HttpServletRequest request, String traceId) {
        return Map.of(
                "method", request.getMethod(),
                "path", request.getRequestURI(),
                "trace_id", traceId
        );
    }

    @GetMapping("/")
    public Map<String, Object> root(HttpServletRequest request) {
        String traceId = UUID.randomUUID().toString();

        return Map.of(
                "status", "success",
                "trace_id", traceId,
                "message", "Welcome to hello_java API",
                "data", Map.of(
                        "service", "hello_java",
                        "version", "0.1.0",
                        "available_routes", List.of("/", "/time", "/health")
                ),
                "request", requestInfo(request, traceId)
        );
    }

    @GetMapping("/time")
    public Map<String, Object> time(HttpServletRequest request) {
        String traceId = UUID.randomUUID().toString();
        Instant now = Instant.now();
        ZonedDateTime nowUtc = now.atZone(ZoneId.of("UTC"));
        ZonedDateTime nowTh = now.atZone(ZoneId.of("Asia/Bangkok"));

        return Map.of(
                "status", "success",
                "trace_id", traceId,
                "message", "Current server time",
                "data", Map.of(
                        "timestamp", now.getEpochSecond(),
                        "datetime_utc", nowUtc.toString(),
                        "datetime_th", nowTh.toString(),
                        "timezone", "Asia/Bangkok",
                        "utc_offset", "+07:00"
                ),
                "request", requestInfo(request, traceId)
        );
    }

    @GetMapping("/health")
    public Map<String, Object> health(HttpServletRequest request) {
        String traceId = UUID.randomUUID().toString();

        return Map.of(
                "status", "success",
                "trace_id", traceId,
                "message", "Service is healthy",
                "data", Map.of(
                        "service", "hello_java",
                        "healthy", true
                ),
                "request", requestInfo(request, traceId)
        );
    }
}
