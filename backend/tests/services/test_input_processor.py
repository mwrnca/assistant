from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.base import Base
from app.models.input import Input
from app.repositories.input_repository import InputRepository
from app.services.input_processor import InputProcessor


def test_process_pending_marks_completed():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    repository = InputRepository(db)
    repository.create(source="TEXT", content="Test input")

    processor = InputProcessor(repository)
    result = processor.process_pending()

    assert result is not None
    assert result.status == "COMPLETED"
