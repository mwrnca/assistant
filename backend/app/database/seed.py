from sqlalchemy import inspect, text

from app.database.base import Base
from app.database.session import engine

import app.models


def create_tables():
    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    if "inputs" not in inspector.get_table_names():
        return

    existing_columns = {column["name"] for column in inspector.get_columns("inputs")}
    if "created_at" not in existing_columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE inputs ADD COLUMN created_at TIMESTAMP"))
    if "processed_at" not in existing_columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE inputs ADD COLUMN processed_at TIMESTAMP"))