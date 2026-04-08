"""Fixtures compartidas: BD en memoria, cliente HTTP y helpers de auth."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.seed import seed_categories

# SQLite en memoria para tests (no necesita PostgreSQL)
TEST_DB_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    """Recrear tablas y seeds antes de cada test."""
    Base.metadata.create_all(bind=engine)
    db = TestSession()
    seed_categories(db)
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_token(client):
    """Registrar un usuario de prueba y devolver su token."""
    response = client.post("/api/auth/register", json={
        "name": "Test",
        "surname": "User",
        "birthdate": "2008-05-15",
        "email": "test@example.com",
        "password": "securepass123",
    })
    return response.json()["token"]


@pytest.fixture
def auth_header(auth_token):
    """Header de autorizacion listo para usar."""
    return {"Authorization": f"Bearer {auth_token}"}
