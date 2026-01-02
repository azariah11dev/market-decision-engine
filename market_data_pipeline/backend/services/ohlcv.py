import pandas as pd
import yfinance as yf
from datetime import date
from typing import List, Dict, Any

class OHLCVMarketInfo:
    VALID_INTERVALS = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
    def __init__(self, ticker: str):
        if not ticker or not isinstance(ticker, str):
            raise ValueError("Ticker cannot be empty")
        self.ticker = ticker

    def get_ohlcv_data(self, start_date: date, end_date: date, interval: str) -> List[Dict[str, Any]]:

        if interval not in self.VALID_INTERVALS:
                raise ValueError(f"Invalid interval: {interval}")
            
        df = yf.download(
                self.ticker,
                start=start_date,
                end=end_date,
                interval=interval,
                progress=False
        )

        if df.empty:
        # retry by shifting start_date forward by 1 day
            new_start = (pd.to_datetime(start_date) + pd.Timedelta(days=1)).date()
            df = yf.download(
                 self.ticker,
                 start=new_start,
                 end=end_date,
                 interval=interval,
                 progress=False
        )
        #If still empty, raise error
        if df.empty:
            raise ValueError(f"No OHLCV data returned for ticker {self.ticker} in the given date range.")
        
        """
        yfinance sometimes returns MultiIndex column names (e.g. ('Open','AAPL'))
        depending on interval and date range, even for a single ticker.
        This breaks FastAPI/Pydantic validation because the schema expects flat names.
        Flatten columns to ensure consistent single-level names.
        """
        # flatten multi-index columns if they exist
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

        df.reset_index(inplace=True) #convert index to column

        # normalize column names to lowercase
        df.columns = [col.lower() for col in df.columns]

        #convert datetime to date
        df["date"] = pd.to_datetime(df["date"]).dt.date

        df["ticker"] = self.ticker #add ticker column

        return df.to_dict(orient="records")
