import logging
from datetime import datetime
from pathlib import Path

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[2]
SQL_DIR = BASE_DIR / "sql"


def extract_table(
    engine: Engine,
    sql_filename: str,
    table_name: str,
    watermark_column: str,
    modified_since: datetime | None = None,
) -> pd.DataFrame:
    sql_path = SQL_DIR / sql_filename
    base_query = sql_path.read_text(encoding="utf-8").rstrip().rstrip(";")

    if modified_since is not None:
        query = f"{base_query}\nWHERE {watermark_column} > :modified_since"
        params = {"modified_since": modified_since}
    else:
        query = base_query
        params = {}

    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn, params=params, dtype_backend="numpy_nullable")

    logger.info("%s: %s linhas extraídas", table_name, len(df))
    return df
