import pytest
from fastapi.testclient import TestClient

from api.service.main import app


@pytest.fixture
def client() -> TestClient:
    """Fixture for the unit test client."""
    client = TestClient(
        app=app,
        headers={
            "User-Agent": "UnitTestClient/1.0",
            "X-Is-Test": "true",
        },
    )
    return client
