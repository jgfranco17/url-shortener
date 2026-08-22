"""Main runtime wiring."""

import logging

from fastapi import FastAPI

from api.core.internal.config import load_configuration_from_env, setup_logging
from api.core.internal.middleware import ProcessTimeMiddleware

logger = logging.getLogger(__name__)


config = load_configuration_from_env()
setup_logging(config.log_level)


app = FastAPI(
    title="URL Shortener API",
    description="A simple URL shortener API built with FastAPI.",
)

app.add_middleware(ProcessTimeMiddleware)


@app.get("/")
def index():
    """Root endpoint for the URL Shortener API."""
    return {"message": "Welcome to my URL Shortener API!"}


@app.get("/healthz")
def health_check():
    """Health check endpoint to verify the API is running."""
    logger.debug("Health check endpoint called")
    return {"status": "healthy"}
