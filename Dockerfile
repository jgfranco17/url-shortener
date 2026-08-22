# syntax=docker/dockerfile:1
FROM python:3.13-alpine AS base

ENV UV_PROJECT_ENVIRONMENT=/usr/local
ENV UV_LINK_MODE=copy
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

FROM base AS builder

RUN apk add --no-cache build-base curl git

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock /backend/
WORKDIR /backend

RUN uv --version \
    && uv sync --no-dev --locked --no-progress --quiet

COPY api/ /backend/api/

FROM builder AS app

WORKDIR /backend
EXPOSE 8080

CMD ["uvicorn", "api.service.main:app", "--host", "0.0.0.0", "--port", "8080"]

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/healthz || exit 1
