from fastapi import FastAPI
from backend.routes.quotes import router

app = FastAPI(title="Market Decision Engine", version="1.0")

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the market decision engine API!",
            "docs": "/docs for API documentation",
            "health": "/health for health check"}

@app.get("/health")
def health_check():
    return {"status": "ok"}