use axum::{
    extract::{OriginalUri, State},
    http::Method,
    routing::get,
    Json, Router,
};
use chrono::{FixedOffset, Utc};
use serde::Serialize;
use std::path::PathBuf;
use tokio::{
    fs::{create_dir_all, OpenOptions},
    io::AsyncWriteExt,
    sync::mpsc::{unbounded_channel, UnboundedReceiver, UnboundedSender},
};
use uuid::Uuid;

const SERVICE_NAME: &str = "hello_rust";
const EVENT_LOG_PATH: &str = "events/request-events.jsonl";

#[derive(Clone)]
struct AppState {
    event_tx: UnboundedSender<AppEvent>,
}

#[derive(Serialize)]
struct ApiResponse<T> {
    status: &'static str,
    trace_id: String,
    message: &'static str,
    event_status: &'static str,
    data: T,
    request: RequestInfo,
}

#[derive(Serialize, Clone)]
struct RequestInfo {
    method: String,
    path: String,
    trace_id: String,
}

#[derive(Serialize)]
struct WelcomeData {
    service: &'static str,
    version: &'static str,
    architecture: &'static str,
    event_log_file: &'static str,
    available_routes: Vec<&'static str>,
}

#[derive(Serialize)]
struct TimeData {
    timestamp: i64,
    datetime_utc: String,
    datetime_th: String,
    timezone: &'static str,
    utc_offset: &'static str,
}

#[derive(Serialize)]
struct HealthData {
    service: &'static str,
    healthy: bool,
    event_consumer: &'static str,
}

#[derive(Serialize, Clone)]
struct AppEvent {
    event_id: String,
    event_type: &'static str,
    emitted_at_utc: String,
    service: &'static str,
    trace_id: String,
    request: RequestInfo,
    data: EventData,
}

#[derive(Serialize, Clone)]
struct EventData {
    route: String,
    response_message: &'static str,
    response_timestamp: i64,
}

fn request_info(method: &Method, uri: &OriginalUri, trace_id: &str) -> RequestInfo {
    RequestInfo {
        method: method.to_string(),
        path: uri.0.path().to_string(),
        trace_id: trace_id.to_string(),
    }
}

fn publish_event(
    state: &AppState,
    event_type: &'static str,
    trace_id: &str,
    request: &RequestInfo,
    response_message: &'static str,
) -> bool {
    state
        .event_tx
        .send(AppEvent {
            event_id: Uuid::new_v4().to_string(),
            event_type,
            emitted_at_utc: Utc::now().to_rfc3339(),
            service: SERVICE_NAME,
            trace_id: trace_id.to_string(),
            request: request.clone(),
            data: EventData {
                route: request.path.clone(),
                response_message,
                response_timestamp: Utc::now().timestamp(),
            },
        })
        .is_ok()
}

async fn event_consumer(mut event_rx: UnboundedReceiver<AppEvent>, log_path: PathBuf) {
    if let Some(parent) = log_path.parent() {
        if let Err(error) = create_dir_all(parent).await {
            eprintln!("failed to create event log directory: {error}");
            return;
        }
    }

    let mut log_file = match OpenOptions::new()
        .create(true)
        .append(true)
        .open(&log_path)
        .await
    {
        Ok(file) => file,
        Err(error) => {
            eprintln!("failed to open event log file: {error}");
            return;
        }
    };

    while let Some(event) = event_rx.recv().await {
        match serde_json::to_string(&event) {
            Ok(json_line) => {
                if let Err(error) = log_file.write_all(format!("{json_line}\n").as_bytes()).await {
                    eprintln!("failed to write event log: {error}");
                }
            }
            Err(error) => eprintln!("failed to serialize event: {error}"),
        }
    }
}

async fn root(
    State(state): State<AppState>,
    method: Method,
    uri: OriginalUri,
) -> Json<ApiResponse<WelcomeData>> {
    let trace_id = Uuid::new_v4().to_string();
    let request = request_info(&method, &uri, &trace_id);
    let event_status = if publish_event(
        &state,
        "root_requested",
        &trace_id,
        &request,
        "Welcome to hello_rust API",
    ) {
        "queued"
    } else {
        "dropped"
    };

    Json(ApiResponse {
        status: "success",
        trace_id: trace_id.clone(),
        message: "Welcome to hello_rust API",
        event_status,
        data: WelcomeData {
            service: SERVICE_NAME,
            version: env!("CARGO_PKG_VERSION"),
            architecture: "request-response + event consumer",
            event_log_file: EVENT_LOG_PATH,
            available_routes: vec!["/", "/time", "/health"],
        },
        request,
    })
}

async fn time(
    State(state): State<AppState>,
    method: Method,
    uri: OriginalUri,
) -> Json<ApiResponse<TimeData>> {
    let now = Utc::now();
    let thailand_tz = FixedOffset::east_opt(7 * 60 * 60).unwrap();
    let thailand_now = now.with_timezone(&thailand_tz);
    let trace_id = Uuid::new_v4().to_string();
    let request = request_info(&method, &uri, &trace_id);
    let event_status = if publish_event(
        &state,
        "time_requested",
        &trace_id,
        &request,
        "Current server time",
    ) {
        "queued"
    } else {
        "dropped"
    };

    Json(ApiResponse {
        status: "success",
        trace_id: trace_id.clone(),
        message: "Current server time",
        event_status,
        data: TimeData {
            timestamp: now.timestamp(),
            datetime_utc: now.to_rfc3339(),
            datetime_th: thailand_now.to_rfc3339(),
            timezone: "Asia/Bangkok",
            utc_offset: "+07:00",
        },
        request,
    })
}

async fn health(
    State(state): State<AppState>,
    method: Method,
    uri: OriginalUri,
) -> Json<ApiResponse<HealthData>> {
    let trace_id = Uuid::new_v4().to_string();
    let request = request_info(&method, &uri, &trace_id);
    let event_status = if publish_event(
        &state,
        "health_requested",
        &trace_id,
        &request,
        "Service is healthy",
    ) {
        "queued"
    } else {
        "dropped"
    };

    Json(ApiResponse {
        status: "success",
        trace_id: trace_id.clone(),
        message: "Service is healthy",
        event_status,
        data: HealthData {
            service: SERVICE_NAME,
            healthy: true,
            event_consumer: "async file logger",
        },
        request,
    })
}

#[tokio::main]
async fn main() {
    let (event_tx, event_rx) = unbounded_channel();
    let state = AppState { event_tx };

    tokio::spawn(event_consumer(event_rx, PathBuf::from(EVENT_LOG_PATH)));

    let app = Router::new()
        .route("/", get(root))
        .route("/time", get(time))
        .route("/health", get(health))
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("127.0.0.1:3000")
        .await
        .unwrap();

    axum::serve(listener, app).await.unwrap();
}
