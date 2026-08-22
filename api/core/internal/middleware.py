import logging
from collections.abc import Awaitable, Callable
from time import perf_counter_ns

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger(__name__)


type RequestHandler = Callable[[Request], Awaitable[Response]]


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    """Middleware class to process request duration and outgoing responses."""

    async def dispatch(self, request: Request, call_next: RequestHandler) -> Response:
        start_time = perf_counter_ns()
        response = await call_next(request)
        process_time = (perf_counter_ns() - start_time) / 1_000_000
        response.headers["X-Process-Time-MS"] = f"{process_time}ms"
        return response
