from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from crisisops_example.core.database import Base, get_db
from crisisops_example.main import app


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSession = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )
    Base.metadata.create_all(bind=engine)

    def override_get_db() -> Generator[Session, None, None]:
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def test_register_resource_starts_available(client: TestClient) -> None:
    response = client.post(
        "/resources",
        json={
            "name": "Ambulancia 03",
            "type": "AMBULANCE",
            "location": "La Serena",
        },
    )

    assert response.status_code == 201

    body = response.json()
    assert body["id"] is not None
    assert body["name"] == "Ambulancia 03"
    assert body["type"] == "AMBULANCE"
    assert body["status"] == "AVAILABLE"
    assert body["location"] == "La Serena"


def test_register_resource_rejects_empty_name(client: TestClient) -> None:
    response = client.post(
        "/resources",
        json={
            "name": "",
            "type": "AMBULANCE",
            "location": "La Serena",
        },
    )

    assert response.status_code == 422
