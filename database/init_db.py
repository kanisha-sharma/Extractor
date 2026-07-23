from sqlalchemy import create_engine, text

from config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)

from database import models
from database.db import Base, engine


def create_database():

    default_engine = create_engine(
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres",
        isolation_level="AUTOCOMMIT"
    )

    with default_engine.connect() as conn:

        result = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname=:dbname"),
            {"dbname": DB_NAME}
        )

        exists = result.scalar()

        if not exists:
            conn.execute(text(f'CREATE DATABASE "{DB_NAME}"'))
            print(f"Database '{DB_NAME}' created successfully.")
        else:
            print(f"Database '{DB_NAME}' already exists.")


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully.")