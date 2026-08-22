import logging

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=True, env_prefix="APP_")
    log_level: str = "INFO"


def load_configuration_from_env() -> Settings:
    """Load configuration from environment variables."""
    settings = Settings()
    logger.debug("Configuration loaded from environment")
    return settings


def setup_logging(log_level: str) -> None:
    """Set up logging configuration based on the provided log level.

    Args:
        log_level (str): Log level setting string

    Raises:
        EnvironmentError: If the provided log level string is invalid.
    """
    numeric_level = logging.INFO
    match log_level.upper():
        case "CRITICAL":
            numeric_level = logging.CRITICAL
        case "ERROR":
            numeric_level = logging.ERROR
        case "WARNING":
            numeric_level = logging.WARNING
        case "INFO":
            numeric_level = logging.INFO
        case "DEBUG":
            numeric_level = logging.DEBUG
        case _:
            raise OSError(f"Invalid logging level: {log_level}")
    logging.basicConfig(
        format="[%(asctime)s][%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=numeric_level,
    )
    logger.debug(f"Logging configured with level: {log_level}")
