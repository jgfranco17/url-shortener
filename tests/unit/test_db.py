import logging

import pytest
from pydantic import ValidationError

from api.core.db.client import InMemoryDatabaseClient, retrieve_database
from api.core.db.models import DatabaseClient, UrlAliasRecord

pytestmark = pytest.mark.unit


class TestUrlAliasRecord:
    def test_creates_valid_record(self) -> None:
        record = UrlAliasRecord(alias="short", url="https://example.com")
        assert record.alias == "short"
        assert record.url == "https://example.com"

    def test_rejects_missing_alias(self) -> None:
        with pytest.raises(ValidationError):
            UrlAliasRecord(url="https://example.com")  # type: ignore[call-arg]

    def test_rejects_missing_url(self) -> None:
        with pytest.raises(ValidationError):
            UrlAliasRecord(alias="short")  # type: ignore[call-arg]

    def test_equality(self) -> None:
        a = UrlAliasRecord(alias="x", url="https://a.com")
        b = UrlAliasRecord(alias="x", url="https://a.com")
        assert a == b

    def test_inequality_on_alias(self) -> None:
        a = UrlAliasRecord(alias="x", url="https://a.com")
        b = UrlAliasRecord(alias="y", url="https://a.com")
        assert a != b

    def test_inequality_on_url(self) -> None:
        a = UrlAliasRecord(alias="x", url="https://a.com")
        b = UrlAliasRecord(alias="x", url="https://b.com")
        assert a != b


class TestDatabaseClientAbstract:
    def test_cannot_instantiate_abstract_class(self) -> None:
        with pytest.raises(TypeError):
            DatabaseClient()  # type: ignore[abstract]


class TestInMemoryDatabaseClientInit:
    def test_default_max_records(self) -> None:
        client = InMemoryDatabaseClient()
        assert client._max_records == 1_000

    def test_custom_max_records(self) -> None:
        client = InMemoryDatabaseClient(max_records=50)
        assert client._max_records == 50

    def test_storage_starts_empty(self) -> None:
        client = InMemoryDatabaseClient()
        assert client._storage == {}

    def test_is_database_client_subclass(self) -> None:
        assert issubclass(InMemoryDatabaseClient, DatabaseClient)


class TestInMemoryDatabaseClientConnect:
    def test_connect_logs_info(self, caplog: pytest.LogCaptureFixture) -> None:
        client = InMemoryDatabaseClient()
        with caplog.at_level(logging.INFO, logger="api.core.db.client"):
            client.connect()
        assert "Connected to in-memory database" in caplog.text

    def test_connect_does_not_raise(self) -> None:
        client = InMemoryDatabaseClient()
        client.connect()


class TestInMemoryDatabaseClientDisconnect:
    def test_disconnect_logs_info(self, caplog: pytest.LogCaptureFixture) -> None:
        client = InMemoryDatabaseClient()
        with caplog.at_level(logging.INFO, logger="api.core.db.client"):
            client.disconnect()
        assert "Disconnected from in-memory database" in caplog.text

    def test_disconnect_does_not_raise(self) -> None:
        client = InMemoryDatabaseClient()
        client.disconnect()


class TestInMemoryDatabaseClientGetByAlias:
    @pytest.fixture
    def client(self) -> InMemoryDatabaseClient:
        return InMemoryDatabaseClient()

    def test_returns_none_when_alias_missing(
        self, client: InMemoryDatabaseClient
    ) -> None:
        assert client.get_by_alias("nonexistent") is None

    def test_returns_record_for_existing_alias(
        self, client: InMemoryDatabaseClient
    ) -> None:
        record = UrlAliasRecord(alias="gh", url="https://github.com")
        client.register_alias(record)
        result = client.get_by_alias("gh")
        assert result == record

    def test_returned_record_has_correct_alias(
        self, client: InMemoryDatabaseClient
    ) -> None:
        client.register_alias(UrlAliasRecord(alias="abc", url="https://abc.com"))
        result = client.get_by_alias("abc")
        assert result is not None
        assert result.alias == "abc"

    def test_returned_record_has_correct_url(
        self, client: InMemoryDatabaseClient
    ) -> None:
        client.register_alias(UrlAliasRecord(alias="abc", url="https://abc.com"))
        result = client.get_by_alias("abc")
        assert result is not None
        assert result.url == "https://abc.com"

    def test_missing_alias_logs_warning(
        self, client: InMemoryDatabaseClient, caplog: pytest.LogCaptureFixture
    ) -> None:
        with caplog.at_level(logging.WARNING, logger="api.core.db.client"):
            client.get_by_alias("ghost")
        assert "ghost" in caplog.text

    def test_lookup_is_case_sensitive(self, client: InMemoryDatabaseClient) -> None:
        client.register_alias(UrlAliasRecord(alias="ABC", url="https://abc.com"))
        assert client.get_by_alias("abc") is None
        assert client.get_by_alias("ABC") is not None

    def test_does_not_return_record_for_different_alias(
        self, client: InMemoryDatabaseClient
    ) -> None:
        client.register_alias(UrlAliasRecord(alias="a", url="https://a.com"))
        assert client.get_by_alias("b") is None


class TestInMemoryDatabaseClientRegisterAlias:
    @pytest.fixture
    def client(self) -> InMemoryDatabaseClient:
        return InMemoryDatabaseClient()

    def test_returns_true_on_success(self, client: InMemoryDatabaseClient) -> None:
        record = UrlAliasRecord(alias="x", url="https://x.com")
        assert client.register_alias(record) is True

    def test_stores_record(self, client: InMemoryDatabaseClient) -> None:
        record = UrlAliasRecord(alias="x", url="https://x.com")
        client.register_alias(record)
        assert client._storage["x"] == "https://x.com"

    def test_overwrites_existing_alias(self, client: InMemoryDatabaseClient) -> None:
        client.register_alias(UrlAliasRecord(alias="x", url="https://first.com"))
        client.register_alias(UrlAliasRecord(alias="x", url="https://second.com"))
        assert client._storage["x"] == "https://second.com"

    def test_returns_false_when_at_capacity(self) -> None:
        client = InMemoryDatabaseClient(max_records=2)
        client.register_alias(UrlAliasRecord(alias="a", url="https://a.com"))
        client.register_alias(UrlAliasRecord(alias="b", url="https://b.com"))
        result = client.register_alias(UrlAliasRecord(alias="c", url="https://c.com"))
        assert result is False

    def test_does_not_store_record_when_at_capacity(self) -> None:
        client = InMemoryDatabaseClient(max_records=1)
        client.register_alias(UrlAliasRecord(alias="a", url="https://a.com"))
        client.register_alias(UrlAliasRecord(alias="b", url="https://b.com"))
        assert "b" not in client._storage

    def test_capacity_check_logs_error(self, caplog: pytest.LogCaptureFixture) -> None:
        client = InMemoryDatabaseClient(max_records=0)
        with caplog.at_level(logging.ERROR, logger="api.core.db.client"):
            client.register_alias(UrlAliasRecord(alias="x", url="https://x.com"))
        assert "Maximum number of records reached" in caplog.text

    def test_accepts_records_up_to_max(self) -> None:
        client = InMemoryDatabaseClient(max_records=3)
        for i in range(3):
            result = client.register_alias(
                UrlAliasRecord(alias=str(i), url=f"https://{i}.com")
            )
            assert result is True
        assert len(client._storage) == 3

    def test_multiple_distinct_aliases_stored_independently(
        self, client: InMemoryDatabaseClient
    ) -> None:
        client.register_alias(UrlAliasRecord(alias="a", url="https://a.com"))
        client.register_alias(UrlAliasRecord(alias="b", url="https://b.com"))
        assert client._storage["a"] == "https://a.com"
        assert client._storage["b"] == "https://b.com"


class TestRetrieveDatabase:
    def test_yields_database_client(self) -> None:
        gen = retrieve_database()
        db = next(gen)
        assert isinstance(db, DatabaseClient)
        with pytest.raises(StopIteration):
            next(gen)

    def test_yields_in_memory_client(self) -> None:
        gen = retrieve_database()
        db = next(gen)
        assert isinstance(db, InMemoryDatabaseClient)
        with pytest.raises(StopIteration):
            next(gen)

    def test_disconnect_called_on_exit(self, caplog: pytest.LogCaptureFixture) -> None:
        gen = retrieve_database()
        next(gen)
        with (
            caplog.at_level(logging.INFO, logger="api.core.db.client"),
            pytest.raises(StopIteration),
        ):
            next(gen)
        assert "Disconnected from in-memory database" in caplog.text
