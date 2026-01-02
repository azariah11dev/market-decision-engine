from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from sqlalchemy import select
from backend.routers.quotes import ohlcv_route
from backend.models.ohlcv_db import create_db_and_tables, get_async_session, OHLCVDataDB
from backend.routers.update import ohlcv_db_route
from sqlalchemy.ext.asyncio import AsyncSession

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(title="Market Decision Engine", version="1.0", lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Welcome to the market decision engine API!",
            "docs": "/docs for API documentation",
            "health": "/health for health check",
            "ohlcv_fetch": "/db/{ticker} to obtain existing market info on stocks",
            "ohlcv_fetch_limited": "/db/{ticker}?limit=(int 1 - ...) to obtain limited existing market info on stocks"}

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