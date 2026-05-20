"""Fixtures compartidas por los tests."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """Cliente HTTP de pruebas para la API."""
    return TestClient(app)
