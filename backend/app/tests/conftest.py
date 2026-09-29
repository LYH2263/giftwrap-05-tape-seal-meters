import pytest
from fastapi.testclient import TestClient
from app import db, seed
from app.main import app


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test.db")
    seed.init_db()
    with TestClient(app) as c:
        yield c
