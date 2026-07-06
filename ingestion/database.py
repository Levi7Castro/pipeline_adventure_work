from functools import lru_cache
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from ingestion.config import SQLSERVER, POSTGRES


@lru_cache(maxsize=1)
def get_sqlserver_engine() -> Engine:
    connection_string = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={SQLSERVER['host']},{SQLSERVER['port']};"
        f"DATABASE={SQLSERVER['database']};"
        f"UID={SQLSERVER['user']};"
        f"PWD={SQLSERVER['password']};"
        "TrustServerCertificate=yes;"
    )
    return create_engine(
        f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_string)}",
        pool_pre_ping=True,
    )


@lru_cache(maxsize=1)
def get_postgres_engine() -> Engine:
    user = quote_plus(POSTGRES["user"])
    password = quote_plus(POSTGRES["password"])
    host = POSTGRES["host"]
    port = POSTGRES["port"]
    database = POSTGRES["database"]
    return create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}",
        pool_pre_ping=True,
    )
