# **Market Data Ingestion Pipeline**
A modular FastAPI + PostgreSQL pipeline for historical OHLCV market data.

This project implements a production-shaped ingestion pipeline focused on raw data capture, idempotent staging loads, and clean API access for downstream systems.

# **Features**
## *OHLCV Fetching (yfinance)*
- Interval validation
- Multi‑index flattening
- Date normalization
- Retry logic for empty frames
- Clean dict output for downstream processing
## *PostgreSQL Staging Load*
- Async SQLAlchemy engine
- UPSERT logic (ON CONFLICT DO NOTHING)
- Composite key on (ticker, date)
- Fully idempotent ingestion
## *FastAPI Service Layer*
- PUT /db/{ticker} → ingest OHLCV into staging
- GET /db/{ticker} → retrieve all rows
- GET /db/{ticker}?limit=N → retrieve limited rows
- GET /health → health check
- GET / → API index
## *Idempotent Ingestion*
Idempotency is enforced via a composite primary key and `ON CONFLICT DO NOTHING`, allowing safe re-runs without duplicate rows.

## *Raw CSV storage (planned)*
Raw OHLCV data will be stored under:
./raw/{ticker}.csv
This layer will be dynamic, supporting:
- Versioned snapshots
- Partitioned storage
- Incremental updates
- Schema evolution
- Multi‑ticker batching
Implementation planned for the next development session.

# **Docker Setup**
- PostgreSQL runs inside Docker for reproducible development.
    - ## Connect to Postgres inside the container
        - docker exec -it market_postgres psql -U postgres -d marketdb

    - ## List tables
        - \dt

    - ## Inspect staging table
        - SELECT * FROM market_ohlcv LIMIT 20;
