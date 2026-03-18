package com.example.hello_java;

public record EventData(
        String route,
        String response_message,
        long response_timestamp
) {
}
