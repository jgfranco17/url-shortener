import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from api.core.db.client import retrieve_database
from api.core.db.models import DatabaseClient, UrlAliasRecord
from api.core.handlers.encoding import encode_text
from api.core.models.params import ShortenRequestParams

logger = logging.getLogger(__name__)

v0_router = APIRouter(tags=["v0"], prefix="/v0")

_db_client_dependency = Depends(retrieve_database)


@v0_router.post("/shorten", status_code=HTTPStatus.OK)
async def shorten_url(
    params: ShortenRequestParams, db_client: DatabaseClient = _db_client_dependency
) -> dict[str, str]:
    """Shorten a given URL."""
    _validate_request(params)
    key = encode_text(params.url)
    record = UrlAliasRecord(alias=params.alias, url=key)
    db_client.register_alias(record)

    logger.info(f"Registered alias '{params.alias}' for URL '{params.url}'")
    return {
        "status": "success",
        "key": key,
        "alias": params.alias,
    }


def _validate_request(params: ShortenRequestParams) -> None:
    """Validate the request parameters."""
    if not params.url:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="No URL provided")
    if not params.alias:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="No alias provided"
        )
