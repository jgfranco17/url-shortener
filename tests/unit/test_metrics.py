from http import HTTPStatus

from fastapi.testclient import TestClient

from api.observability.metrics import REQUEST_COUNT, REQUEST_LATENCY


def test_metrics_endpoint_exposes_prometheus_format(client: TestClient) -> None:
    response = client.get("/metrics")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    assert "http_requests_total" in response.text
    assert "http_request_duration_seconds" in response.text


def test_request_count_increments_on_success(client: TestClient) -> None:
    before = _request_count("GET", "/healthz", HTTPStatus.OK)
    client.get("/healthz")
    after = _request_count("GET", "/healthz", HTTPStatus.OK)
    assert after == before + 1


def test_request_count_labels_error_status_code(client: TestClient) -> None:
    before = _request_count("GET", "/v0/greet", HTTPStatus.BAD_REQUEST)
    response = client.get("/v0/greet")
    assert response.status_code == 400
    after = _request_count("GET", "/v0/greet", HTTPStatus.BAD_REQUEST)
    assert after == before + 1


def test_request_count_uses_route_template_not_raw_url(client: TestClient) -> None:
    """Requests with different query params should collapse to the same path label."""
    before = _request_count("GET", "/v0/greet", HTTPStatus.OK)
    client.get("/v0/greet?name=Alice")
    client.get("/v0/greet?name=Bob")
    after = _request_count("GET", "/v0/greet", HTTPStatus.OK)
    assert after == before + 2


def test_request_count_falls_back_to_raw_path_for_unmatched_routes(
    client: TestClient,
) -> None:
    before = _request_count("GET", "/does-not-exist", HTTPStatus.NOT_FOUND)
    response = client.get("/does-not-exist")
    assert response.status_code == 404
    after = _request_count("GET", "/does-not-exist", HTTPStatus.NOT_FOUND)
    assert after == before + 1


def test_request_latency_recorded(client: TestClient) -> None:
    before = _request_latency_count("GET", "/healthz")
    client.get("/healthz")
    after = _request_latency_count("GET", "/healthz")
    assert after == before + 1


def _request_count(method: str, path: str, status_code: int) -> float:
    """Read the current value of the request counter for a given label set."""
    labels = {"method": method, "path": path, "status_code": str(status_code)}
    for family in REQUEST_COUNT.collect():
        for sample in family.samples:
            if sample.name == "http_requests_total" and sample.labels == labels:
                return sample.value
    return 0.0


def _request_latency_count(method: str, path: str) -> float:
    """Read the current observation count of the latency histogram for a label set."""
    labels = {"method": method, "path": path}
    for family in REQUEST_LATENCY.collect():
        metric_under_test = "http_request_duration_seconds_count"
        for sample in family.samples:
            if sample.name == metric_under_test and sample.labels == labels:
                return sample.value
    return 0.0
