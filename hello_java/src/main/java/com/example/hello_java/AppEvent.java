package com.example.hello_java;

public record AppEvent(
        String event_id,
        String event_type,
        String emitted_at_utc,
        String service,
        String trace_id,
        RequestInfo request,
        EventData data
) {
}
