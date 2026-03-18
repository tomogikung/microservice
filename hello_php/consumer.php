<?php

declare(strict_types=1);

const EVENT_QUEUE_DIR = __DIR__ . '/events/pending';
const EVENT_LOG_PATH = __DIR__ . '/events/request-events.jsonl';

if (!is_dir(EVENT_QUEUE_DIR)) {
    mkdir(EVENT_QUEUE_DIR, 0775, true);
}

if (!is_dir(dirname(EVENT_LOG_PATH))) {
    mkdir(dirname(EVENT_LOG_PATH), 0775, true);
}

$eventFiles = glob(EVENT_QUEUE_DIR . '/*.json') ?: [];
sort($eventFiles);

$consumed = 0;

foreach ($eventFiles as $eventFile) {
    $eventPayload = trim((string) file_get_contents($eventFile));

    if ($eventPayload === '') {
        unlink($eventFile);
        continue;
    }

    $written = file_put_contents(EVENT_LOG_PATH, $eventPayload . PHP_EOL, FILE_APPEND | LOCK_EX);

    if ($written === false) {
        fwrite(STDERR, "Failed to append event log for {$eventFile}\n");
        continue;
    }

    unlink($eventFile);
    $consumed++;
}

echo "Consumed {$consumed} event(s)\n";
