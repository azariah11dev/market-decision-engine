from fastapi import APIRouter, HTTPException, Depends
from backend.models.ohlcv_db import OHLCVDataDB, get_async_session
from backend.services.ohlcv import OHLCVMarketInfo
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from datetime import date

ohlcv_db_route = APIRouter(prefix="/db", tags=["db"])

@ohlcv_db_route.put("/{ticker}")
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
        create_rows = create_rows.on_conflict_do_update(
            index_elements=["ticker", "date"],
            set_= {
                "open": create_rows.excluded.open,
                "high": create_rows.excluded.high,
                "low": create_rows.excluded.low,
                "close": create_rows.excluded.close,
                "volume": create_rows.excluded.volume,
                "dividends": create_rows.excluded.dividends,
                "stock_split": create_rows.excluded.stock_split
            }
        )
        await session.execute(create_rows)
        await session.commit()
        return {"status": "ok",
                "inserted": len(rows)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
