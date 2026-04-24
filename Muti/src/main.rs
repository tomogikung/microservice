use axum::{Router, routing::get};
use std::env;

async fn root() -> &'static str {
    "Hello from Axum"
}

async fn health() -> &'static str {
    "OK"
}

#[tokio::main]
async fn main() {
    let host = env::var("APP_HOST").unwrap_or_else(|_| "0.0.0.0".to_string());
    let port = env::var("PORT").unwrap_or_else(|_| "3009".to_string());
    let address = format!("{host}:{port}");

    let app = Router::new()
        .route("/", get(root))
        .route("/health", get(health));

    let listener = tokio::net::TcpListener::bind(&address)
        .await
        .unwrap_or_else(|error| panic!("bind {address} failed: {error}"));

    println!("listening on http://{address}");
    axum::serve(listener, app).await.unwrap();
}
