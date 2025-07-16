# Haven Development Justfile
# Run `just --list` to see all available commands

# Default recipe shows available commands
default:
    @just --list

# Python environment
venv := ".venv"
python := venv + "/bin/python"
pip := venv + "/bin/pip"

# Create virtual environment
bootstrap:
    python3.12 -m venv {{ venv }}
    {{ pip }} install --upgrade pip
    {{ pip }} install -e ".[dev]"
    @echo "✅ Environment ready! Run 'source {{ venv }}/bin/activate' to activate"

# Install all dependencies
install:
    {{ pip }} install -e ".[dev,docs]"

# Update dependencies
update:
    {{ pip }} install --upgrade pip
    {{ pip }} install --upgrade -e ".[dev,docs]"

# Run the application in development mode
run:
    {{ python }} -m haven.main

# Run with specific environment
run-env env="local":
    {{ python }} -m haven.main +environment={{ env }}

# Database commands
db-up:
    docker compose up -d postgres
    @echo "⏳ Waiting for PostgreSQL to be ready..."
    @sleep 3
    @echo "✅ PostgreSQL is running"

db-down:
    docker compose down

db-reset:
    docker compose down -v
    docker compose up -d postgres
    @sleep 3
    @echo "✅ Database reset complete"

# Run migrations
db-migrate:
    alembic upgrade head

# Create a new migration
db-make message:
    alembic revision --autogenerate -m "{{ message }}"

# Show migration history
db-history:
    alembic history --verbose

# Show current migration
db-current:
    alembic current

# Downgrade database
db-downgrade steps="1":
    alembic downgrade -{{ steps }}

# Quality checks
lint:
    {{ python }} -m ruff check .

lint-fix:
    {{ python }} -m ruff check --fix .
    {{ python }} -m ruff format .

format:
    {{ python }} -m ruff format .

type:
    {{ python }} -m pyright

# Run all quality checks
check: lint type test-fast

# Testing
test:
    {{ python }} -m pytest

test-fast:
    {{ python }} -m pytest -m "not slow"

test-cov:
    {{ python }} -m pytest --cov=haven --cov-report=html

test-watch:
    {{ python }} -m pytest-watch

# Run specific test file
test-file file:
    {{ python }} -m pytest {{ file }}

# Documentation
docs:
    mkdocs build

docs-serve:
    mkdocs serve --dev-addr localhost:8001

docs-deploy:
    mkdocs gh-deploy --force

# Development utilities
shell:
    {{ python }} -m asyncio

# Database console
db-console:
    docker compose exec postgres psql -U haven -d haven

# Show logs
logs:
    docker compose logs -f

# Clean up generated files
clean:
    rm -rf build/ dist/ *.egg-info/
    find . -type d -name __pycache__ -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete
    rm -rf .coverage htmlcov/ .pytest_cache/
    rm -rf .ruff_cache/ .mypy_cache/ .pyright/
    rm -rf site/
    rm -rf diff-out*/ diff-demo*/
    rm -f server.log

# Docker commands
docker-build tag="latest":
    ./scripts/build-docker.sh --tag {{ tag }}

docker-build-multi:
    ./scripts/build-docker.sh --multi-arch

docker-run:
    docker run -p 8080:8080 --env-file .env haven:latest

docker-push registry tag="latest":
    ./scripts/build-docker.sh --push --registry {{ registry }} --tag {{ tag }}

docker-size:
    @docker images haven --format "table {{ '{{' }}.Repository{{ '}}' }}\t{{ '{{' }}.Tag{{ '}}' }}\t{{ '{{' }}.Size{{ '}}' }}"

# Pre-commit setup
pre-commit-install:
    pre-commit install

pre-commit-run:
    pre-commit run --all-files

# Demo command (placeholder for future implementation)
demo:
    @echo "🎯 Demo functionality will be implemented per feature"
    @echo "Run specific demos with: just demo-<feature>"

# Demo: Diff Generation API
demo-diff-generation:
    @echo "🔍 Diff Generation API Demo"
    @echo "This demo shows how to use the FastAPI diff generation endpoints"
    @echo ""
    @if ! curl -s http://localhost:8080/health > /dev/null 2>&1; then \
        echo "❌ Server is not running. Starting server..."; \
        echo "   Run 'just run' in another terminal first"; \
        exit 1; \
    fi
    @{{ python }} scripts/demo-diff-generation.py

# Add a new entity (scaffolding helper)
add-entity name:
    @echo "🏗️  Scaffolding entity: {{ name }}"
    @echo "TODO: Implement entity scaffolding"
    @echo "- Create domain/entities/{{ name }}.py"
    @echo "- Create application/use_cases/{{ name }}_use_cases.py"
    @echo "- Create infrastructure/repositories/{{ name }}_repository.py"
    @echo "- Create interface/api/routes/{{ name }}_routes.py"
    @echo "- Create tests for all layers"

# Show current environment info
info:
    @echo "Python: $({{ python }} --version)"
    @echo "Environment: {{ venv }}"
    @echo "Working directory: $(pwd)"
    @{{ python }} -m pip list | grep -E "(fastapi|sqlalchemy|strawberry|pydantic)"

# Full CI simulation
ci: clean bootstrap check docs
    @echo "✅ All CI checks passed!"