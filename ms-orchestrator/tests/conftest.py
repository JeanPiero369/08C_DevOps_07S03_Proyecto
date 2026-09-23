import pytest
from fastapi.testclient import TestClient

from main import app

USERS_URL = "http://localhost:8001"


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def users_url():
    return USERS_URL
