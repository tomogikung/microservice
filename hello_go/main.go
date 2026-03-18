package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"time"
)

const (
	serviceName  = "hello_go"
	port         = "3001"
	eventLogPath = "events/request-events.jsonl"
)

type AppState struct {
	eventCh chan AppEvent
}

type APIResponse struct {
	Status      string      `json:"status"`
	TraceID     string      `json:"trace_id"`
	Message     string      `json:"message"`
	EventStatus string      `json:"event_status"`
	Data        interface{} `json:"data"`
	Request     RequestInfo `json:"request"`
}

type RequestInfo struct {
	Method  string `json:"method"`
	Path    string `json:"path"`
	TraceID string `json:"trace_id"`
}

type WelcomeData struct {
	Service         string   `json:"service"`
	Version         string   `json:"version"`
	Architecture    string   `json:"architecture"`
	EventLogFile    string   `json:"event_log_file"`
	AvailableRoutes []string `json:"available_routes"`
}

type TimeData struct {
	Timestamp   int64  `json:"timestamp"`
	DateTimeUTC string `json:"datetime_utc"`
	DateTimeTH  string `json:"datetime_th"`
	Timezone    string `json:"timezone"`
	UTCOffset   string `json:"utc_offset"`
}

type HealthData struct {
	Service       string `json:"service"`
	Healthy       bool   `json:"healthy"`
	EventConsumer string `json:"event_consumer"`
}

type AppEvent struct {
	EventID      string      `json:"event_id"`
	EventType    string      `json:"event_type"`
	EmittedAtUTC string      `json:"emitted_at_utc"`
	Service      string      `json:"service"`
	TraceID      string      `json:"trace_id"`
	Request      RequestInfo `json:"request"`
	Data         EventData   `json:"data"`
}

type EventData struct {
	Route             string `json:"route"`
	ResponseMessage   string `json:"response_message"`
	ResponseTimestamp int64  `json:"response_timestamp"`
}

func newTraceID() string {
	return time.Now().UTC().Format("20060102T150405.000000000Z07:00")
}

func requestInfo(r *http.Request, traceID string) RequestInfo {
	return RequestInfo{
		Method:  r.Method,
		Path:    r.URL.Path,
		TraceID: traceID,
	}
}

func publishEvent(state *AppState, eventType string, request RequestInfo, responseMessage string) string {
	event := AppEvent{
		EventID:      newTraceID(),
		EventType:    eventType,
		EmittedAtUTC: time.Now().UTC().Format(time.RFC3339),
		Service:      serviceName,
		TraceID:      request.TraceID,
		Request:      request,
		Data: EventData{
			Route:             request.Path,
			ResponseMessage:   responseMessage,
			ResponseTimestamp: time.Now().UTC().Unix(),
		},
	}

	select {
	case state.eventCh <- event:
		return "queued"
	default:
		return "dropped"
	}
}

func eventConsumer(eventCh <-chan AppEvent, logPath string) {
	if err := os.MkdirAll(filepath.Dir(logPath), 0o755); err != nil {
		log.Printf("failed to create event log directory: %v", err)
		return
	}

	logFile, err := os.OpenFile(logPath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0o644)
	if err != nil {
		log.Printf("failed to open event log file: %v", err)
		return
	}
	defer logFile.Close()

	for event := range eventCh {
		jsonLine, err := json.Marshal(event)
		if err != nil {
			log.Printf("failed to marshal event: %v", err)
			continue
		}

		if _, err := logFile.Write(append(jsonLine, '\n')); err != nil {
			log.Printf("failed to write event log: %v", err)
		}
	}
}

func writeJSON(w http.ResponseWriter, statusCode int, payload interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(statusCode)

	if err := json.NewEncoder(w).Encode(payload); err != nil {
		http.Error(w, "internal server error", http.StatusInternalServerError)
	}
}

func rootHandler(state *AppState) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/" {
			http.NotFound(w, r)
			return
		}

		traceID := newTraceID()
		request := requestInfo(r, traceID)
		eventStatus := publishEvent(state, "root_requested", request, "Welcome to hello_go API")

		response := APIResponse{
			Status:      "success",
			TraceID:     traceID,
			Message:     "Welcome to hello_go API",
			EventStatus: eventStatus,
			Data: WelcomeData{
				Service:         serviceName,
				Version:         "0.1.0",
				Architecture:    "request-response + event consumer",
				EventLogFile:    eventLogPath,
				AvailableRoutes: []string{"/", "/time", "/health"},
			},
			Request: request,
		}

		writeJSON(w, http.StatusOK, response)
	}
}

func timeHandler(state *AppState) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		traceID := newTraceID()
		request := requestInfo(r, traceID)
		nowUTC := time.Now().UTC()
		thailandTZ := time.FixedZone("Asia/Bangkok", 7*60*60)
		nowTH := nowUTC.In(thailandTZ)
		eventStatus := publishEvent(state, "time_requested", request, "Current server time")

		response := APIResponse{
			Status:      "success",
			TraceID:     traceID,
			Message:     "Current server time",
			EventStatus: eventStatus,
			Data: TimeData{
				Timestamp:   nowUTC.Unix(),
				DateTimeUTC: nowUTC.Format(time.RFC3339),
				DateTimeTH:  nowTH.Format(time.RFC3339),
				Timezone:    "Asia/Bangkok",
				UTCOffset:   "+07:00",
			},
			Request: request,
		}

		writeJSON(w, http.StatusOK, response)
	}
}

func healthHandler(state *AppState) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		traceID := newTraceID()
		request := requestInfo(r, traceID)
		eventStatus := publishEvent(state, "health_requested", request, "Service is healthy")

		response := APIResponse{
			Status:      "success",
			TraceID:     traceID,
			Message:     "Service is healthy",
			EventStatus: eventStatus,
			Data: HealthData{
				Service:       serviceName,
				Healthy:       true,
				EventConsumer: "async file logger",
			},
			Request: request,
		}

		writeJSON(w, http.StatusOK, response)
	}
}

func main() {
	state := &AppState{
		eventCh: make(chan AppEvent, 128),
	}

	go eventConsumer(state.eventCh, eventLogPath)

	http.HandleFunc("/", rootHandler(state))
	http.HandleFunc("/time", timeHandler(state))
	http.HandleFunc("/health", healthHandler(state))

	log.Printf("Server running at http://127.0.0.1:%s", port)
	if err := http.ListenAndServe("127.0.0.1:"+port, nil); err != nil {
		log.Fatal(err)
	}
}
