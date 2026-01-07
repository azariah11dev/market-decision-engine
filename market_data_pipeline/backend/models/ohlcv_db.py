from sqlalchemy import Column, String, DateTime, Float, Date, PrimaryKeyConstraint
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func
from typing import AsyncGenerator

DATABASE_URL = "postgresql+asyncpg://postgres:deep_vlaue@localhost:5432/marketdb"

class Base(DeclarativeBase):
    pass

class OHLCVDataDB(Base):
    __tablename__ = "market_ohlcv"

    ticker = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    dividends = Column(Float, nullable=False, default=0.0)
    stock_split = Column(Float, nullable=False, default=0.0)

    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        PrimaryKeyConstraint("ticker", "date", name="pk_ticker_date"),
    )

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

#create tables
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


#Dependency for FastAPI
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session