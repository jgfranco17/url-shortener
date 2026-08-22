import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)

base_router = APIRouter()


@base_router.get("/")
def index():
    """Root endpoint for the URL Shortener API."""
    return {"message": "Welcome to my URL Shortener API!"}


@base_router.get("/healthz")
def health_check():
    """Health check endpoint to verify the API is running."""
    logger.debug("Health check endpoint called")
    return {"status": "healthy"}
