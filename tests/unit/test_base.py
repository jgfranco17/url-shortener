import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit
def test_index(client: TestClient) -> None:
    """Test the index endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to my URL Shortener API!"}
