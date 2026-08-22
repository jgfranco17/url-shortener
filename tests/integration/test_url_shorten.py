from tests.integration.utils import IntegrationClient
from tests.shared.flags import mark_as_integration_test


@mark_as_integration_test("FUNCTIONAL")
def test_url_shorten_success(integration_client: IntegrationClient) -> None:
    """Test the URL shorten endpoint."""
    payload = {"url": "https://example.com", "alias": "Shortened"}
    response = integration_client.post("/v0/shorten", json=payload)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    shorten_response = response.json()
    assert shorten_response["status"] == "success"
    assert shorten_response["alias"] == "Shortened"
