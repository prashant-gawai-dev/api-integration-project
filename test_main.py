from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=engine)

client = TestClient(app)


def test_create_config():
    response = client.post(
        "/configs",
        json={
            "name": "test_api",
            "endpoint": "https://example.com",
            "auth_type": "none",
            "timeout": 10,
            "rate_limit": 50,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["received"]["name"] == "test_api"


def test_get_one_config():
    response = client.get("/getConfig/999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "config not found"


def test_create_config_invalid_data():
    response = client.post("/configs", json={"name": "incomplete"})
    assert response.status_code == 422
