from dotenv import load_dotenv
import os

load_dotenv()

SQLSERVER = {
    "host": os.getenv("SQLSERVER_HOST"),
    "port": os.getenv("SQLSERVER_PORT"),
    "database": os.getenv("SQLSERVER_DB"),
    "user": os.getenv("SQLSERVER_USER"),
    "password": os.getenv("SQLSERVER_PASSWORD"),
}

POSTGRES = {
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
    "database": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}
