import os

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.base import Base
from app.database.dependencies import get_db
from app.models.input import Input
from app.main import app


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_create_input_returns_pending_status(client):
    response = client.post(
        "/api/v1/input",
        json={"source": "TEXT", "content": "Buy milk tomorrow"},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["status"] == "PENDING"
    assert isinstance(payload["id"], int)


def test_upload_input_accepts_files_for_voice_sources(client):
    response = client.post(
        "/api/v1/input/upload",
        data={"source": "VOICE", "content": "Transcript placeholder"},
        files={"file": ("clip.wav", b"fake-audio-bytes", "audio/wav")},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["source"] == "VOICE"
    assert payload["status"] == "PENDING"
    assert "clip.wav" in payload["content"]
