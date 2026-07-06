import argparse
import logging
import sys
from datetime import datetime

from sqlalchemy import text
from sqlalchemy.engine import Engine

from ingestion.database import get_sqlserver_engine, get_postgres_engine
from ingestion.extract.extract_adventure import extract_sales_order_header
from ingestion.load.load_adventure import load_dataframe

logger = logging.getLogger(__name__)

TABLE_NAME = "sales_order_header"
BRONZE_SCHEMA = "bronze"
WATERMARK_COLUMN = "ModifiedDate"


def get_watermark(pg_engine: Engine, table_name: str) -> datetime | None:
    with pg_engine.begin() as conn:
        conn.execute(text('CREATE SCHEMA IF NOT EXISTS "_meta"'))
        conn.execute(
            text(
                'CREATE TABLE IF NOT EXISTS "_meta".ingestion_watermark ('
                "  table_name text PRIMARY KEY,"
                "  last_value timestamp,"
                "  updated_at timestamptz DEFAULT now()"
                ")"
            )
        )
        row = conn.execute(
            text(
                'SELECT last_value FROM "_meta".ingestion_watermark '
                "WHERE table_name = :t"
            ),
            {"t": table_name},
        ).fetchone()

    return row[0] if row else None


def set_watermark(pg_engine: Engine, table_name: str, value: datetime) -> None:
    with pg_engine.begin() as conn:
        conn.execute(
            text(
                'INSERT INTO "_meta".ingestion_watermark '
                "(table_name, last_value, updated_at) "
                "VALUES (:t, :v, now()) "
                "ON CONFLICT (table_name) DO UPDATE "
                "SET last_value = EXCLUDED.last_value, updated_at = now()"
            ),
            {"t": table_name, "v": value},
        )


def run(full_refresh: bool = False) -> int:
    sqlserver_engine = get_sqlserver_engine()
    pg_engine = get_postgres_engine()

    if full_refresh:
        modified_since = None
        logger.info("Modo full refresh: ignorando watermark")
    else:
        modified_since = get_watermark(pg_engine, TABLE_NAME)
        logger.info("Watermark atual: %s", modified_since or "nenhum (full load)")

    df = extract_sales_order_header(
        engine=sqlserver_engine,
        modified_since=modified_since,
    )

    if df.empty:
        logger.info("Nenhuma linha nova. Encerrando sem carga.")
        return 0

    new_watermark = df[WATERMARK_COLUMN].max()

    rows = load_dataframe(
        df,
        table_name=TABLE_NAME,
        schema=BRONZE_SCHEMA,
        if_exists="replace" if full_refresh else "append",
        engine=pg_engine,
    )

    set_watermark(pg_engine, TABLE_NAME, new_watermark)
    logger.info("Watermark atualizado para %s", new_watermark)

    return rows


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    parser = argparse.ArgumentParser(description="Ingestão SalesOrderHeader → bronze")
    parser.add_argument(
        "--full-refresh",
        action="store_true",
        help="Recarrega tudo do zero, ignorando o watermark",
    )
    args = parser.parse_args()

    try:
        rows = run(full_refresh=args.full_refresh)
    except Exception:
        logger.exception("Falha na ingestão de SalesOrderHeader")
        return 1

    logger.info("Ingestão concluída: %s linhas", rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
