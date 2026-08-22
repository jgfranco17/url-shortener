from dataclasses import dataclass
from typing import Any
from urllib.parse import urljoin

from requests import Session


@dataclass(frozen=True)
class RecordedTestRequest:
    """A dataclass to record test requests made during integration tests."""

    method: str
    endpoint: str


class IntegrationClient:
    """A custom test client for integration tests."""

    def __init__(self, base_url: str):
        self._base_url = base_url
        self._session = Session()
        self._requested_urls = []

        headers = {
            "Accept": "application/json",
            "User-Agent": "IntegrationTestClient/1.0",
            "X-Is-Test": "true",
        }
        for key, value in headers.items():
            self._session.headers.update({key: value})

    def _make_request(self, method: str, endpoint: str, **kwargs: Any):
        """Wrapped helper to make HTTP requests with the test client."""
        url = urljoin(self._base_url, endpoint)
        response = self._session.request(method.upper(), url, **kwargs)
        record = RecordedTestRequest(method=method.upper(), endpoint=endpoint)
        self._requested_urls.append(record)
        return response

    def get(self, endpoint: str, **kwargs: Any):
        return self._make_request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs: Any):
        return self._make_request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs: Any):
        return self._make_request("PUT", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs: Any):
        return self._make_request("DELETE", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs: Any):
        return self._make_request("PATCH", endpoint, **kwargs)
