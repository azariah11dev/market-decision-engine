from fastapi import APIRouter, HTTPException
from backend.schemas.schemas import OHLCVData
from backend.services.ohlcv import OHLCVMarketInfo
from datetime import date
from typing import List

ohlcv_route = APIRouter(prefix="/quotes", tags=["quotes"])

@ohlcv_route.post("/{ticker}", response_model=List[OHLCVData])
async def get_ohlcv_data(ticker: str, start_date: date, end_date: date, interval: str):
    try:
        services_ohlcv = OHLCVMarketInfo(ticker)
        return services_ohlcv.get_ohlcv_data(start_date, end_date, interval)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))