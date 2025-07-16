# Docker operations module
# Access these commands with: just docker::<command>

# Show help for docker module
[private]
help:
    @echo "🐳 Docker Commands"
    @echo ""
    @echo "  docker::up        Start containers"
    @echo "  docker::down      Stop containers"
    @echo "  docker::logs      View logs"
    @echo "  docker::shell     Shell into container"
    @echo "  docker::rebuild   Rebuild images"
    @echo "  docker::reset     Full reset"
    @echo ""

# Start all containers
up:
    docker compose up

# Start containers in background
up-d:
    docker compose up -d

# Stop all containers
down:
    docker compose down

# View logs (optionally specify service)
logs service="":
    docker compose logs -f {{ service }}

# Shell into API container
shell:
    docker compose exec api /bin/bash

# Python REPL in container
shell-python:
    docker compose exec api python -m asyncio

# Show running containers
ps:
    docker compose ps

# Rebuild containers
rebuild:
    docker compose build --no-cache

# Full reset (containers + volumes)
reset:
    docker compose down -v
    docker compose up -d

# Run tests in container
test:
    docker compose run --rm api pytest tests/ --no-cov

# Run linting in container
lint:
    docker compose run --rm api ruff check .

# Run type checking in container
type-check:
    docker compose run --rm api pyright

# Clean Docker resources
clean:
    docker compose down
    docker system prune -f

# Build Docker image
build tag="latest":
    ./scripts/build-docker.sh --tag {{ tag }}

# Show image sizes
size:
    @docker images haven --format "table {{ '{{' }}.Repository{{ '}}' }}\t{{ '{{' }}.Tag{{ '}}' }}\t{{ '{{' }}.Size{{ '}}' }}"