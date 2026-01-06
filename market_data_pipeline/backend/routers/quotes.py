from fastapi import APIRouter, HTTPException, Depends
from backend.models.ohlcv_db import OHLCVDataDB, get_async_session
from backend.schemas.schemas import OHLCVRespose
from backend.services.ohlcv import OHLCVMarketInfo
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from datetime import date
from typing import List

ohlcv_route = APIRouter(prefix="/quotes", tags=["quotes"])

@ohlcv_route.post("/{ticker}", response_model=List[OHLCVRespose])
async def get_ohlcv_data(ticker: str, start_date: date, end_date: date, interval: str):
    try:
        services_ohlcv = OHLCVMarketInfo(ticker)
        return services_ohlcv.get_ohlcv_data(start_date, end_date, interval)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@ohlcv_route.post("/{ticker}")
async def save_ohlcv(
    ticker: str,
    start_date: date,
    end_date: date,
    interval: str,
    session: AsyncSession = Depends(get_async_session)):
    try:
        service = OHLCVMarketInfo(ticker)
        rows = service.get_ohlcv_data(start_date, end_date, interval)
        create_rows = insert(OHLCVDataDB).values(rows)
        create_rows = create_rows.on_conflict_do_nothing(
            index_elements=["ticker", "date"]
        )
        await session.execute(create_rows)
        await session.commit()
        return {"status": "ok",
                "inserted": len(rows)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))