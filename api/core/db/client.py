import logging
from collections.abc import Iterator

from api.core.db.models import DatabaseClient, UrlAliasRecord
from api.core.internal.config import AppEnvironment, load_configuration_from_env

logger = logging.getLogger(__name__)


class InMemoryDatabaseClient(DatabaseClient):
    """In-memory implementation of the DatabaseClient."""

    def __init__(self, max_records: int = 1_000) -> None:
        self._storage: dict[str, str] = {}
        self._max_records = max_records

    def connect(self) -> None:
        """Establish a connection to the in-memory database."""
        logger.info("Connected to in-memory database.")

    def disconnect(self) -> None:
        """Close the connection to the in-memory database."""
        logger.info("Disconnected from in-memory database.")

    def get_by_alias(self, alias: str) -> UrlAliasRecord | None:
        """Retrieve a record by its alias."""
        url = self._storage.get(alias)
        if url is not None:
            return UrlAliasRecord(alias=alias, url=url)
        logger.warning(f"No record found for alias '{alias}'")
        return None

    def register_alias(self, record: UrlAliasRecord) -> bool:
        """Register a new alias with its corresponding URL."""
        if len(self._storage) >= self._max_records:
            logger.error("Maximum number of records reached.")
            return False
        self._storage[record.alias] = record.url
        return True


def retrieve_database() -> Iterator[DatabaseClient]:
    """Dependency function to get the database client."""
    config = load_configuration_from_env()
    if config.environment in {AppEnvironment.LOCAL, AppEnvironment.DEVELOPMENT}:
        db_client = InMemoryDatabaseClient()
    else:
        raise RuntimeError(
            f"Database client for environment '{config.environment}' is not implemented."
        )
    db_client.connect()
    try:
        yield db_client
    finally:
        db_client.disconnect()
