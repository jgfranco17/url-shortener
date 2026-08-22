import os
from typing import Final

import pytest

ENV_RUN_INTEGRATION_TESTS: Final[str] = "RUN_INTEGRATION_TESTS"


def mark_as_integration_test(category: str) -> pytest.MarkDecorator:
    """Skip integration tests if the env marker is not set."""
    env_is_integration_run = os.getenv(ENV_RUN_INTEGRATION_TESTS, "false")
    return pytest.mark.skipif(
        env_is_integration_run.lower() not in {"true", "1", "yes"},
        reason=f"Skipping {category} integration test",
    )
