import logging
from datetime import datetime
from pathlib import Path

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

from ingestion.database import get_sqlserver_engine

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[2]
SQL_PATH = BASE_DIR / "sql" / "SalesOrderHeader.sql"


def extract_sales_order_header(
    engine: Engine | None = None,
    modified_since: datetime | None = None,
) -> pd.DataFrame:
    query = SQL_PATH.read_text(encoding="utf-8")
    engine = engine or get_sqlserver_engine()

    with engine.connect() as conn:
        df = pd.read_sql(
            text(query),
            conn,
            params={"modified_since": modified_since},
            dtype_backend="numpy_nullable",
        )

    logger.info("SalesOrderHeader: %s linhas extraídas", len(df))
    return df
