import logging

import pytest

from api.core.internal.config import (
    AppEnvironment,
    Settings,
    load_configuration_from_env,
    setup_logging,
)

pytestmark = pytest.mark.unit


@pytest.fixture(autouse=True)
def reset_root_logger():
    """Restore root logger state after each test so basicConfig can be re-applied."""
    original_level = logging.root.level
    original_handlers = logging.root.handlers[:]
    yield
    logging.root.setLevel(original_level)
    logging.root.handlers = original_handlers


class TestSetupLogging:
    @pytest.mark.parametrize(
        "level_str, expected",
        [
            ("CRITICAL", logging.CRITICAL),
            ("ERROR", logging.ERROR),
            ("WARNING", logging.WARNING),
            ("INFO", logging.INFO),
            ("DEBUG", logging.DEBUG),
            ("critical", logging.CRITICAL),
            ("info", logging.INFO),
        ],
    )
    def test_valid_levels(self, level_str: str, expected: int) -> None:
        logging.root.handlers.clear()
        setup_logging(level_str)
        assert logging.root.level == expected

    def test_invalid_level_raises_os_error(self) -> None:
        with pytest.raises(OSError, match="Invalid logging level"):
            setup_logging("VERBOSE")


class TestLoadConfigurationFromEnv:
    def test_returns_settings_instance(self) -> None:
        settings = load_configuration_from_env()
        assert isinstance(settings, Settings)

    def test_default_log_level(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("APP_LOG_LEVEL", raising=False)
        settings = load_configuration_from_env()
        assert settings.log_level == "INFO"

    def test_env_override_log_level(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("APP_LOG_LEVEL", "DEBUG")
        settings = load_configuration_from_env()
        assert settings.log_level == "DEBUG"

    def test_default_environment(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("APP_ENVIRONMENT", raising=False)
        settings = load_configuration_from_env()
        assert settings.environment == AppEnvironment.DEVELOPMENT

    def test_env_override_environment(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("APP_ENVIRONMENT", "local")
        settings = load_configuration_from_env()
        assert settings.environment == AppEnvironment.LOCAL
