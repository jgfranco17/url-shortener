PORT := env("APP_PORT", "8080")

# List out available commands
_default:
    @just --list --unsorted

# Execute installation
setup:
    @echo "Setting up project..."
    uv sync

# Launch API in debug mode
start-local:
    @echo "Running main app..."
    uv run uvicorn api.service.main:app --host 0.0.0.0 --port {{ PORT }} --reload

# Run Pytest unit tests
pytest *args:
	@echo "Running unittest suite..."
	uv run pytest {{ args }}

# Build Docker image for the API
build tag="latest":
    #!/usr/bin/env bash
    export TAG={{ tag }}
    echo "Building Docker image (tag: $TAG)"
    docker compose build
