import logging
from datetime import datetime, timezone

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

from ingestion.database import get_postgres_engine

logger = logging.getLogger(__name__)

MAX_BIND_PARAMS = 65535


def load_dataframe(
    df: pd.DataFrame,
    table_name: str,
    schema: str = "bronze",
    if_exists: str = "append",
    engine: Engine | None = None,
    add_load_metadata: bool = True,
) -> int:
    if df.empty:
        logger.info("%s.%s: DataFrame vazio, nada a carregar", schema, table_name)
        return 0

    engine = engine or get_postgres_engine()

    if add_load_metadata:
        df = df.copy()
        df["_loaded_at"] = datetime.now(timezone.utc)

    n_cols = max(1, len(df.columns))
    safe_chunksize = max(1, MAX_BIND_PARAMS // n_cols)
    chunksize = min(5000, safe_chunksize)

    with engine.begin() as conn:
        conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))
        df.to_sql(
            name=table_name,
            con=conn,
            schema=schema,
            if_exists=if_exists,
            index=False,
            method="multi",
            chunksize=chunksize,
        )

    logger.info(
        "%s.%s: %s linhas carregadas (%s)",
        schema, table_name, len(df), if_exists,
    )
    return len(df)
