import argparse
import logging
import sys
from datetime import datetime

from sqlalchemy import text
from sqlalchemy.engine import Engine

from ingestion.database import get_sqlserver_engine, get_postgres_engine
from ingestion.extract.extract_generic import extract_table
from ingestion.load.load_adventure import load_dataframe
from ingestion.tables import TABLES

logger = logging.getLogger(__name__)

BRONZE_SCHEMA = "bronze"


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


def run_table(
    table_cfg: dict,
    sqlserver_engine: Engine,
    pg_engine: Engine,
    full_refresh: bool = False,
) -> int:
    """Executa a ingestão de uma tabela: extract -> load -> watermark."""
    name = table_cfg["name"]
    sql_filename = table_cfg["sql_filename"]
    watermark_column = table_cfg["watermark_column"]

    # Algumas tabelas têm um bug conhecido no filtro incremental via
    # parâmetro bindado (pyodbc) e precisam sempre de full-refresh.
    # Ver comentário em ingestion/tables.py.
    table_force_full = table_cfg.get("force_full_refresh", False)
    effective_full_refresh = full_refresh or table_force_full

    if effective_full_refresh:
        modified_since = None
        reason = "flag --full-refresh" if full_refresh else "force_full_refresh na config"
        logger.info("[%s] Modo full refresh (%s): ignorando watermark", name, reason)
    else:
        modified_since = get_watermark(pg_engine, name)
        logger.info(
            "[%s] Watermark atual: %s",
            name, modified_since or "nenhum (full load)",
        )

    df = extract_table(
        engine=sqlserver_engine,
        sql_filename=sql_filename,
        table_name=name,
        watermark_column=watermark_column,
        modified_since=modified_since,
    )

    if df.empty:
        logger.info("[%s] Nenhuma linha nova. Encerrando sem carga.", name)
        return 0

    new_watermark = df[watermark_column].max()

    rows = load_dataframe(
        df,
        table_name=name,
        schema=BRONZE_SCHEMA,
        if_exists="replace" if effective_full_refresh else "append",
        engine=pg_engine,
    )

    set_watermark(pg_engine, name, new_watermark)
    logger.info("[%s] Watermark atualizado para %s", name, new_watermark)

    return rows


def run(full_refresh: bool = False) -> dict[str, int]:
    """Itera todas as tabelas configuradas em TABLES.

    Uma tabela que falhar é logada e pulada; as demais continuam.
    Retorna um dict {table_name: rows_loaded} para as que tiveram sucesso.
    """
    sqlserver_engine = get_sqlserver_engine()
    pg_engine = get_postgres_engine()

    results: dict[str, int] = {}
    failed: list[str] = []

    for table_cfg in TABLES:
        name = table_cfg["name"]
        try:
            rows = run_table(table_cfg, sqlserver_engine, pg_engine, full_refresh)
            results[name] = rows
        except Exception:
            logger.exception("[%s] Falha na ingestão, pulando para a próxima", name)
            failed.append(name)

    if failed:
        logger.warning("Tabelas com falha: %s", ", ".join(failed))

    return results


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    parser = argparse.ArgumentParser(description="Ingestão multi-tabela → bronze")
    parser.add_argument(
        "--full-refresh",
        action="store_true",
        help="Recarrega tudo do zero, ignorando o watermark",
    )
    args = parser.parse_args()

    results = run(full_refresh=args.full_refresh)

    total = sum(results.values())
    logger.info(
        "Ingestão concluída: %s tabelas processadas, %s linhas no total",
        len(results), total,
    )
    for name, rows in results.items():
        logger.info("  - %s: %s linhas", name, rows)

    return 0 if results else 1


if __name__ == "__main__":
    sys.exit(main())