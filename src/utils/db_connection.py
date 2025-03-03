import psycopg2
from sqlalchemy import create_engine
from sqlalchemy import URL

from .settings import (
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DB,
    POSTGRES_SCHEMA,
    POSTGRES_PORT,
    DB_HOST,
)

engine = create_engine(
    URL.create(
        drivername="postgresql+psycopg2",
        username=POSTGRES_USER,  # Ensure it's set correctly
        password=POSTGRES_PASSWORD,
        host=DB_HOST,
        database=POSTGRES_DB,
    ),
    connect_args={"options": f"-c search_path={POSTGRES_SCHEMA}"},
)

connection = psycopg2.connect(
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=DB_HOST,
    port=POSTGRES_PORT,
    options=f"-c search_path={POSTGRES_SCHEMA}",
)
