package com.example.hello_java;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
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
    private final EventService eventService;

    @Autowired
    public ApiController(EventService eventService) {
        this.eventService = eventService;
    }

    @GetMapping("/")
    public Map<String, Object> root(HttpServletRequest request) {
        String traceId = UUID.randomUUID().toString();
        String eventStatus = eventService.publishEvent(
                request,
                "root_requested",
                traceId,
                "Welcome to hello_java API"
        );

        return Map.of(
                "status", "success",
                "trace_id", traceId,
                "message", "Welcome to hello_java API",
                "event_status", eventStatus,
                "data", Map.of(
                        "service", EventService.SERVICE_NAME,
                        "version", "0.1.0",
                        "architecture", "request-response + event consumer",
                        "event_log_file", EventService.EVENT_LOG_FILE,
                        "available_routes", List.of("/", "/time", "/health")
                ),
                "request", eventService.requestInfo(request, traceId)
        );
    }

    @GetMapping("/time")
    public Map<String, Object> time(HttpServletRequest request) {
        String traceId = UUID.randomUUID().toString();
        Instant now = Instant.now();
        ZonedDateTime nowUtc = now.atZone(ZoneId.of("UTC"));
        ZonedDateTime nowTh = now.atZone(ZoneId.of("Asia/Bangkok"));
        String eventStatus = eventService.publishEvent(
                request,
                "time_requested",
                traceId,
                "Current server time"
        );

        return Map.of(
                "status", "success",
                "trace_id", traceId,
                "message", "Current server time",
                "event_status", eventStatus,
                "data", Map.of(
                        "timestamp", now.getEpochSecond(),
                        "datetime_utc", nowUtc.toString(),
                        "datetime_th", nowTh.toString(),
                        "timezone", "Asia/Bangkok",
                        "utc_offset", "+07:00"
                ),
                "request", eventService.requestInfo(request, traceId)
        );
    }

    @GetMapping("/health")
    public Map<String, Object> health(HttpServletRequest request) {
        String traceId = UUID.randomUUID().toString();
        String eventStatus = eventService.publishEvent(
                request,
                "health_requested",
                traceId,
                "Service is healthy"
        );

        return Map.of(
                "status", "success",
                "trace_id", traceId,
                "message", "Service is healthy",
                "event_status", eventStatus,
                "data", Map.of(
                        "service", EventService.SERVICE_NAME,
                        "healthy", true,
                        "event_consumer", "background file logger"
                ),
                "request", eventService.requestInfo(request, traceId)
        );
    }
}
