from pydantic import BaseModel

class OHLCVData(BaseModel):
    ticker: str
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: float