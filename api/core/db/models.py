from abc import ABC, abstractmethod

from pydantic import BaseModel


class UrlAliasRecord(BaseModel):
    """Data model representing a URL alias record."""

    alias: str
    url: str


class DatabaseClient(ABC):
    """Abstract base class for database clients."""

    @abstractmethod
    def connect(self) -> None:
        """Establish a connection to the database."""
        raise NotImplementedError("Subclasses must implement the connect method.")

    @abstractmethod
    def disconnect(self) -> None:
        """Close the connection to the database."""
        raise NotImplementedError("Subclasses must implement the disconnect method.")

    @abstractmethod
    def get_by_alias(self, alias: str) -> UrlAliasRecord | None:
        """Retrieve a record by its alias."""
        raise NotImplementedError("Subclasses must implement the get_by_alias method.")

    @abstractmethod
    def register_alias(self, record: UrlAliasRecord) -> bool:
        """Register a new alias with its corresponding URL."""
        raise NotImplementedError("Subclasses must implement the register_alias method.")
