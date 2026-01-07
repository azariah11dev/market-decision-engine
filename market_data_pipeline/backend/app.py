from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware

from backend.routers.update import ohlcv_db_route
from backend.models.ohlcv_db import create_db_and_tables, get_async_session, OHLCVDataDB
from backend.routers.quotes import ohlcv_route
from backend.routers.performance import performance_route

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(title="Market Decision Engine", version="1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", 
                   "http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the market decision engine API!",
            "docs": "/docs for API documentation",
            "health": "/health for health check",
            "ohlcv_fetch": "/db/{ticker} to obtain existing market info on stocks",
            "ohlcv_fetch_limited": "/db/{ticker}?limit=(int 1 - ...) to obtain limited existing market info on stocks",
            "calculations": "/calculations/{ticker} to find calculation parameters"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@ohlcv_db_route.get("/{ticker}")
async def get_ohlcv(ticker: str,
                    session: AsyncSession = Depends(get_async_session),
                    limit: int=None
):
    try:
        result = await session.execute(
            select(OHLCVDataDB).where(OHLCVDataDB.ticker == ticker)
        )
        rows = result.mappings().all()
        if limit is not None:
            return rows[:limit]
        return rows
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

app.include_router(ohlcv_route)
app.include_router(ohlcv_db_route)
app.include_router(performance_route)