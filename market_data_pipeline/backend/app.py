from fastapi import FastAPI
from backend.routers.quotes import ohlcv_route

app = FastAPI(title="Market Decision Engine", version="1.0")

app.include_router(ohlcv_route)

@app.get("/")
def read_root():
    return {"message": "Welcome to the market decision engine API!",
            "docs": "/docs for API documentation",
            "health": "/health for health check"}

@app.get("/health")
def health_check():
    return {"status": "ok"}