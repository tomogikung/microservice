package com.example.hello_java;

public record RequestInfo(
        String method,
        String path,
        String trace_id
) {
}
