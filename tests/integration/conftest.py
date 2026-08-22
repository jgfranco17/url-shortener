import os
from typing import Final

import pytest

from tests.integration.utils import IntegrationClient

ENV_APP_PORT: Final[str] = "APP_PORT"


@pytest.fixture
def integration_client() -> IntegrationClient:
    """Fixture for the integration test client."""
    port_from_env = os.getenv(ENV_APP_PORT, "8000")
    assert port_from_env.isdigit(), (
        f"{ENV_APP_PORT} env variable must be a valid integer."
    )
    port_used = int(port_from_env)
    assert 1 <= port_used <= 65535, f"{ENV_APP_PORT} must be between 1 and 65535."
    client = IntegrationClient(base_url=f"http://localhost:{port_from_env}")
    return client
