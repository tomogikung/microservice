package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type APIResponse struct {
	Status  string      `json:"status"`
	TraceID string      `json:"trace_id"`
	Message string      `json:"message"`
	Data    interface{} `json:"data"`
	Request RequestInfo `json:"request"`
}

type RequestInfo struct {
	Method  string `json:"method"`
	Path    string `json:"path"`
	TraceID string `json:"trace_id"`
}

type WelcomeData struct {
	Service         string   `json:"service"`
	Version         string   `json:"version"`
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
	Service string `json:"service"`
	Healthy bool   `json:"healthy"`
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

func writeJSON(w http.ResponseWriter, statusCode int, payload interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(statusCode)

	if err := json.NewEncoder(w).Encode(payload); err != nil {
		http.Error(w, "internal server error", http.StatusInternalServerError)
	}
}

func rootHandler(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path != "/" {
		http.NotFound(w, r)
		return
	}

	traceID := newTraceID()

	response := APIResponse{
		Status:  "success",
		TraceID: traceID,
		Message: "Welcome to hello_go API",
		Data: WelcomeData{
			Service:         "hello_go",
			Version:         "0.1.0",
			AvailableRoutes: []string{"/", "/time", "/health"},
		},
		Request: requestInfo(r, traceID),
	}

	writeJSON(w, http.StatusOK, response)
}

func timeHandler(w http.ResponseWriter, r *http.Request) {
	traceID := newTraceID()
	nowUTC := time.Now().UTC()
	thailandTZ := time.FixedZone("Asia/Bangkok", 7*60*60)
	nowTH := nowUTC.In(thailandTZ)

	response := APIResponse{
		Status:  "success",
		TraceID: traceID,
		Message: "Current server time",
		Data: TimeData{
			Timestamp:   nowUTC.Unix(),
			DateTimeUTC: nowUTC.Format(time.RFC3339),
			DateTimeTH:  nowTH.Format(time.RFC3339),
			Timezone:    "Asia/Bangkok",
			UTCOffset:   "+07:00",
		},
		Request: requestInfo(r, traceID),
	}

	writeJSON(w, http.StatusOK, response)
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	traceID := newTraceID()

	response := APIResponse{
		Status:  "success",
		TraceID: traceID,
		Message: "Service is healthy",
		Data: HealthData{
			Service: "hello_go",
			Healthy: true,
		},
		Request: requestInfo(r, traceID),
	}

	writeJSON(w, http.StatusOK, response)
}

func main() {
	http.HandleFunc("/", rootHandler)
	http.HandleFunc("/time", timeHandler)
	http.HandleFunc("/health", healthHandler)

	log.Println("Server running at http://127.0.0.1:3001")
	if err := http.ListenAndServe("127.0.0.1:3001", nil); err != nil {
		log.Fatal(err)
	}
}
