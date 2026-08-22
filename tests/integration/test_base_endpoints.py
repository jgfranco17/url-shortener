from tests.integration.utils import IntegrationClient
from tests.shared.flags import mark_as_integration_test


@mark_as_integration_test("BASE")
def test_index(integration_client: IntegrationClient) -> None:
    """Test the index endpoint."""
    response = integration_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to my URL Shortener API!"}


@mark_as_integration_test("BASE")
def test_health(integration_client: IntegrationClient) -> None:
    """Test the health endpoint."""
    response = integration_client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
