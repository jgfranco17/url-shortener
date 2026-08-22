import logging
from http import HTTPStatus

from fastapi import APIRouter

logger = logging.getLogger(__name__)


v0_router = APIRouter(tags=["v0"], prefix="/v0")


@v0_router.post("/shorten", status_code=HTTPStatus.OK)
async def shorten_url(encoded_url: str) -> dict[str, str]:
    """Shorten a given URL."""
    key = _decode_url(encoded_url)
    return {
        "status": "success",
        "key": key,
    }


def _decode_url(encoded_string: str) -> str:
    """Decode a shortened URL back to its original form."""
    return f"Decoded original URL from '{encoded_string}'"
