package com.example.hello_java;

import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;
import jakarta.servlet.http.HttpServletRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.time.Instant;
import java.util.UUID;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;

@Service
public class EventService {
    public static final String SERVICE_NAME = "hello_java";
    public static final String EVENT_LOG_FILE = "events/request-events.jsonl";

    private static final Logger logger = LoggerFactory.getLogger(EventService.class);

    private final ObjectMapper objectMapper;
    private final BlockingQueue<AppEvent> eventQueue = new LinkedBlockingQueue<>(128);
    private final AtomicBoolean running = new AtomicBoolean(true);
    private final Path eventLogPath = Path.of(EVENT_LOG_FILE);

    private Thread consumerThread;

    public EventService(ObjectMapper objectMapper) {
        this.objectMapper = objectMapper;
    }

    @PostConstruct
    void startConsumer() {
        consumerThread = new Thread(this::consumeLoop, "hello-java-event-consumer");
        consumerThread.setDaemon(true);
        consumerThread.start();
    }

    @PreDestroy
    void stopConsumer() {
        running.set(false);

        if (consumerThread != null) {
            consumerThread.interrupt();
            try {
                consumerThread.join(1000);
            } catch (InterruptedException exception) {
                Thread.currentThread().interrupt();
            }
        }
    }

    public RequestInfo requestInfo(HttpServletRequest request, String traceId) {
        return new RequestInfo(
                request.getMethod(),
                request.getRequestURI(),
                traceId
        );
    }

    public String publishEvent(
            HttpServletRequest request,
            String eventType,
            String traceId,
            String responseMessage
    ) {
        AppEvent event = new AppEvent(
                UUID.randomUUID().toString(),
                eventType,
                Instant.now().toString(),
                SERVICE_NAME,
                traceId,
                requestInfo(request, traceId),
                new EventData(
                        request.getRequestURI(),
                        responseMessage,
                        Instant.now().getEpochSecond()
                )
        );

        return eventQueue.offer(event) ? "queued" : "dropped";
    }

    private void consumeLoop() {
        try {
            Files.createDirectories(eventLogPath.getParent());
        } catch (IOException exception) {
            logger.error("Failed to create event log directory", exception);
            return;
        }

        while (running.get() && !Thread.currentThread().isInterrupted()) {
            try {
                AppEvent event = eventQueue.poll(1, TimeUnit.SECONDS);
                if (event == null) {
                    continue;
                }

                String jsonLine = objectMapper.writeValueAsString(event) + System.lineSeparator();
                Files.writeString(
                        eventLogPath,
                        jsonLine,
                        StandardOpenOption.CREATE,
                        StandardOpenOption.APPEND
                );
            } catch (InterruptedException exception) {
                Thread.currentThread().interrupt();
            } catch (IOException exception) {
                logger.error("Failed to write event log entry", exception);
            }
        }
    }
}
