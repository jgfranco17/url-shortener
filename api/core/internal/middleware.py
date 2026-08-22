import logging
import time
from collections.abc import Awaitable, Callable
from time import perf_counter_ns

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from api.observability.metrics import REQUEST_COUNT, REQUEST_LATENCY

logger = logging.getLogger(__name__)


type DispatchCallable = Callable[[Request], Awaitable[Response]]


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    """Middleware class to process request duration and outgoing responses."""

    async def dispatch(self, request: Request, call_next: DispatchCallable) -> Response:
        start_time = perf_counter_ns()
        response = await call_next(request)
        process_time = (perf_counter_ns() - start_time) / 1_000_000
        response.headers["X-Process-Time-MS"] = f"{process_time}ms"
        return response


class PrometheusMiddleware(BaseHTTPMiddleware):
    """Middleware to collect Prometheus metrics for HTTP requests."""

    @staticmethod
    def _resolve_route_path(request: Request) -> str:
        """Use the matched route template to keep label cardinality low."""
        route = request.scope.get("route")
        return route.path if route else request.url.path

    async def dispatch(self, request: Request, call_next: DispatchCallable) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start_time

        path = self._resolve_route_path(request)
        REQUEST_LATENCY.labels(method=request.method, path=path).observe(duration)
        REQUEST_COUNT.labels(
            method=request.method,
            path=path,
            status_code=response.status_code,
        ).inc()

        return response
