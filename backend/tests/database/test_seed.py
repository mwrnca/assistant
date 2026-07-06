from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.database.seed as seed_module
from app.database.base import Base


def test_create_tables_adds_missing_columns_to_existing_table():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with engine.begin() as connection:
        connection.execute(
            text(
                "CREATE TABLE inputs ("
                "id INTEGER PRIMARY KEY, "
                "source VARCHAR NOT NULL, "
                "content TEXT NOT NULL, "
                "status VARCHAR DEFAULT 'PENDING'"
                ")"
            )
        )

    seed_module.engine = engine
    seed_module.create_tables()

    inspector = inspect(engine)
    columns = {column["name"] for column in inspector.get_columns("inputs")}

    assert {"created_at", "processed_at"}.issubset(columns)
