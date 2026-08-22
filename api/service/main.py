"""Main runtime wiring."""

import logging

from fastapi import FastAPI

from api.core.internal.config import load_configuration_from_env, setup_logging
from api.core.internal.middleware import ProcessTimeMiddleware
from api.service.routes.base.common import base_router
from api.service.routes.v0.shortener import v0_router

logger = logging.getLogger(__name__)


config = load_configuration_from_env()
setup_logging(config.log_level)


app = FastAPI(
    title="URL Shortener API",
    description="A simple URL shortener API built with FastAPI.",
)

app.add_middleware(ProcessTimeMiddleware)
app.include_router(base_router)
app.include_router(v0_router)
