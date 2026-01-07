from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
import pandas as pd
from sqlalchemy import select

from backend.models.ohlcv_db import OHLCVDataDB, get_async_session
from backend.services.calculation import PerformanceCalculator

performance_route = APIRouter(prefix="/calculations", tags=["calculations"])

@performance_route.get("/{ticker}")
async def get_performance(
    ticker: str,
    starting_balance: float,
    start_date: date,
    end_date: date,
    session: AsyncSession = Depends(get_async_session)
):
    # 1. Query Postgres for this ticker
    result = await session.execute(
        select(OHLCVDataDB).where(OHLCVDataDB.ticker == ticker).where(OHLCVDataDB.date >= start_date).where(OHLCVDataDB.date <= end_date).order_by(OHLCVDataDB.date)
    )
    rows = result.mappings().all()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail=f"No OHLCV data found for {ticker} in this date range."
        )
    
    # 2. Convert tp DataFrame
    df = pd.DataFrame(rows)

    # 3. Run your performance calculator
    calc = PerformanceCalculator(
        df=df,
        ticker=ticker,
        start_balance=starting_balance,
        start_date=start_date,
        end_date=end_date,
        )
    
    # 4. Return all metrics
    try:
        return {
        "final amount with dividend reinvested": calc.final_amount_dividend_reinvested(),
        "final amount no reinvested dividends": calc.final_amount_no_reinvestment(),
        "best day": calc.best_day(),
        "three month": calc.three_month(),
        "one year": calc.one_year(),
        "five years": calc.five_years(),
        "ten years": calc.ten_years(),
        "max drawdown": calc.max_drawdown(),
        "gain/loss ratio": calc.gain_loss_ratio(),
        "positive period percentage": calc.positive_period_percentage()
    }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))