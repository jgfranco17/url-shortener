import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.unit


class TestShortenEndpoint:
    def test_returns_200_with_valid_params(self, client: TestClient) -> None:
        response = client.post(
            "/v0/shorten", json={"url": "https://example.com", "alias": "ex"}
        )
        assert response.status_code == 200

    def test_response_contains_status_success(self, client: TestClient) -> None:
        response = client.post(
            "/v0/shorten", json={"url": "https://example.com", "alias": "ex"}
        )
        assert response.json()["status"] == "success"

    def test_response_contains_alias(self, client: TestClient) -> None:
        response = client.post(
            "/v0/shorten", json={"url": "https://example.com", "alias": "ex"}
        )
        assert response.json()["alias"] == "ex"

    def test_response_contains_base64_key(self, client: TestClient) -> None:
        import base64

        url = "https://example.com"
        response = client.post("/v0/shorten", json={"url": url, "alias": "ex"})
        expected_key = base64.b64encode(url.encode()).decode()
        assert response.json()["key"] == expected_key

    def test_empty_url_returns_400(self, client: TestClient) -> None:
        response = client.post("/v0/shorten", json={"url": "", "alias": "ex"})
        assert response.status_code == 400

    def test_empty_alias_returns_400(self, client: TestClient) -> None:
        response = client.post(
            "/v0/shorten", json={"url": "https://example.com", "alias": ""}
        )
        assert response.status_code == 400

    def test_empty_url_error_detail(self, client: TestClient) -> None:
        response = client.post("/v0/shorten", json={"url": "", "alias": "ex"})
        assert "No URL provided" in response.json()["detail"]

    def test_empty_alias_error_detail(self, client: TestClient) -> None:
        response = client.post(
            "/v0/shorten", json={"url": "https://example.com", "alias": ""}
        )
        assert "No alias provided" in response.json()["detail"]


class TestHealthzEndpoint:
    def test_returns_200(self, client: TestClient) -> None:
        response = client.get("/healthz")
        assert response.status_code == 200

    def test_returns_healthy_status(self, client: TestClient) -> None:
        response = client.get("/healthz")
        assert response.json() == {"status": "healthy"}
