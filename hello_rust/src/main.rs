use axum::{
    extract::OriginalUri,
    http::Method,
    routing::get,
    Json, Router,
};
use chrono::{FixedOffset, Utc};
use serde::Serialize;
use uuid::Uuid;

#[derive(Serialize)]
struct ApiResponse<T> {
    status: &'static str,
    trace_id: String,
    message: &'static str,
    data: T,
    request: RequestInfo,
}

#[derive(Serialize)]
struct RequestInfo {
    method: String,
    path: String,
    trace_id: String,
}

#[derive(Serialize)]
struct WelcomeData {
    service: &'static str,
    version: &'static str,
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
}

fn request_info(method: Method, uri: OriginalUri, trace_id: &str) -> RequestInfo {
    RequestInfo {
        method: method.to_string(),
        path: uri.0.path().to_string(),
        trace_id: trace_id.to_string(),
    }
}

async fn root(method: Method, uri: OriginalUri) -> Json<ApiResponse<WelcomeData>> {
    let trace_id = Uuid::new_v4().to_string();

    Json(ApiResponse {
        status: "success",
        trace_id: trace_id.clone(),
        message: "Welcome to hello_rust API",
        data: WelcomeData {
            service: "hello_rust",
            version: env!("CARGO_PKG_VERSION"),
            available_routes: vec!["/", "/time", "/health"],
        },
        request: request_info(method, uri, &trace_id),
    })
}

async fn time(method: Method, uri: OriginalUri) -> Json<ApiResponse<TimeData>> {
    let now = Utc::now();
    let thailand_tz = FixedOffset::east_opt(7 * 60 * 60).unwrap();
    let thailand_now = now.with_timezone(&thailand_tz);
    let trace_id = Uuid::new_v4().to_string();

    Json(ApiResponse {
        status: "success",
        trace_id: trace_id.clone(),
        message: "Current server time",
        data: TimeData {
            timestamp: now.timestamp(),
            datetime_utc: now.to_rfc3339(),
            datetime_th: thailand_now.to_rfc3339(),
            timezone: "Asia/Bangkok",
            utc_offset: "+07:00",
        },
        request: request_info(method, uri, &trace_id),
    })
}

async fn health(method: Method, uri: OriginalUri) -> Json<ApiResponse<HealthData>> {
    let trace_id = Uuid::new_v4().to_string();

    Json(ApiResponse {
        status: "success",
        trace_id: trace_id.clone(),
        message: "Service is healthy",
        data: HealthData {
            service: "hello_rust",
            healthy: true,
        },
        request: request_info(method, uri, &trace_id),
    })
}

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/", get(root))
        .route("/time", get(time))
        .route("/health", get(health));

    let listener = tokio::net::TcpListener::bind("127.0.0.1:3000")
        .await
        .unwrap();

    axum::serve(listener, app).await.unwrap();
}
