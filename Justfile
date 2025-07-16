# Haven Development Justfile
# Run `just --list` to see all available commands

# Default recipe shows available commands
default:
    @just --list

# Directory configuration
api_dir := "apps/api"
web_dir := "apps/web"

# Python environment (relative to api_dir when used with cd)
python := ".venv/bin/python"
pip := ".venv/bin/pip"

# Bootstrap entire monorepo
bootstrap: bootstrap-python bootstrap-web
    @echo "✅ Monorepo bootstrap complete!"

# Create Python virtual environment
bootstrap-python:
    cd {{ api_dir }} && python3.12 -m venv .venv
    cd {{ api_dir }} && .venv/bin/pip install --upgrade pip
    cd {{ api_dir }} && .venv/bin/pip install -e ".[dev]"
    @echo "✅ Python environment ready! Run 'source {{ api_dir }}/.venv/bin/activate' to activate"

# Install Node.js dependencies
bootstrap-web:
    cd {{ web_dir }} && npm install
    @echo "✅ Web environment ready!"

# Install all dependencies
install: install-python install-web
    @echo "✅ All dependencies installed!"

# Install Python dependencies
install-python:
    cd {{ api_dir }} && {{ pip }} install -e ".[dev,docs]"

# Install Web dependencies
install-web:
    cd {{ web_dir }} && npm install

# Update all dependencies
update: update-python update-web
    @echo "✅ All dependencies updated!"

# Update Python dependencies
update-python:
    cd {{ api_dir }} && {{ pip }} install --upgrade pip
    cd {{ api_dir }} && {{ pip }} install --upgrade -e ".[dev,docs]"

# Update Web dependencies
update-web:
    cd {{ web_dir }} && npm update

# Run both API and Web in development mode
run: run-api
    @echo "🚀 Use 'just run-web' in another terminal to start the web client"

# Run API server
run-api:
    cd {{ api_dir }} && {{ python }} -m haven.main

# Run Web development server
run-web:
    cd {{ web_dir }} && npm run dev

# Run with specific environment
run-env env="local":
    cd {{ api_dir }} && {{ python }} -m haven.main +environment={{ env }}

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
    cd {{ api_dir }} && {{ python }} -m alembic upgrade head

# Create a new migration
db-make message:
    cd {{ api_dir }} && {{ python }} -m alembic revision --autogenerate -m "{{ message }}"

# Show migration history
db-history:
    cd {{ api_dir }} && {{ python }} -m alembic history --verbose

# Show current migration
db-current:
    cd {{ api_dir }} && {{ python }} -m alembic current

# Downgrade database
db-downgrade steps="1":
    cd {{ api_dir }} && {{ python }} -m alembic downgrade -{{ steps }}

# Quality checks for all code
lint: lint-python lint-web
    @echo "✅ All linting passed!"

# Python linting
lint-python:
    cd {{ api_dir }} && {{ python }} -m ruff check .

# Web linting
lint-web:
    cd {{ web_dir }} && npm run lint

# Fix linting issues
lint-fix: lint-fix-python lint-fix-web
    @echo "✅ All linting issues fixed!"

lint-fix-python:
    cd {{ api_dir }} && {{ python }} -m ruff check --fix .
    cd {{ api_dir }} && {{ python }} -m ruff format .

lint-fix-web:
    cd {{ web_dir }} && npm run format

# Format all code
format: format-python format-web
    @echo "✅ All code formatted!"

format-python:
    cd {{ api_dir }} && {{ python }} -m ruff format .

format-web:
    cd {{ web_dir }} && npm run format

# Type checking
type: type-python type-web
    @echo "✅ All type checking passed!"

type-python:
    cd {{ api_dir }} && {{ python }} -m pyright

type-web:
    cd {{ web_dir }} && npm run type-check

# Run all quality checks
check: lint type test-fast

# Run all tests
test: test-python test-web
    @echo "✅ All tests passed!"

# Python testing
test-python:
    cd {{ api_dir }} && {{ python }} -m pytest

# Web testing (placeholder for now)
test-web:
    @echo "📝 Web tests not implemented yet"

test-fast: test-fast-python
    @echo "✅ Fast tests passed!"

test-fast-python:
    cd {{ api_dir }} && {{ python }} -m pytest -m "not slow"

# Coverage testing
test-cov: test-cov-python
    @echo "✅ Coverage report generated!"

test-cov-python:
    cd {{ api_dir }} && {{ python }} -m pytest --cov=haven --cov-report=html

# Watch mode testing
test-watch: test-watch-python

test-watch-python:
    cd {{ api_dir }} && {{ python }} -m pytest-watch

# Run specific test file
test-file file:
    cd {{ api_dir }} && {{ python }} -m pytest {{ file }}

# Documentation
docs:
    cd {{ api_dir }} && {{ python }} -m mkdocs build --config-file ../../mkdocs.yml --site-dir ../../site

docs-serve:
    cd {{ api_dir }} && {{ python }} -m mkdocs serve --config-file ../../mkdocs.yml --dev-addr localhost:8001

docs-deploy:
    cd {{ api_dir }} && {{ python }} -m mkdocs gh-deploy --config-file ../../mkdocs.yml --force

# Development utilities
shell:
    cd {{ api_dir }} && {{ python }} -m asyncio

# Database console
db-console:
    docker compose exec postgres psql -U haven -d haven

# Show logs
logs:
    docker compose logs -f

# Clean up generated files
clean: clean-python clean-web
    rm -rf diff-out*/ diff-demo*/
    rm -f server.log
    @echo "✅ All cleaned!"

clean-python:
    cd {{ api_dir }} && rm -rf build/ dist/ *.egg-info/
    find {{ api_dir }} -type d -name __pycache__ -exec rm -rf {} +
    find {{ api_dir }} -type f -name "*.pyc" -delete
    cd {{ api_dir }} && rm -rf .coverage htmlcov/ .pytest_cache/
    cd {{ api_dir }} && rm -rf .ruff_cache/ .mypy_cache/ .pyright/
    cd {{ api_dir }} && rm -rf site/

clean-web:
    cd {{ web_dir }} && rm -rf dist/ node_modules/.cache/
    cd {{ web_dir }} && rm -rf .eslintcache

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

# Demo: View all commits and diffs in browser (single command)
demo-commits:
    ./scripts/demo-commits.sh {{ api_dir }} {{ python }}

# Demo: Diff Generation API (legacy - requires manual server start)
demo-diff-generation:
    ./scripts/demo-diff-generation.sh {{ api_dir }} {{ python }}

# CLI Tools
# List commits from current branch
cli-list-commits:
    cd {{ api_dir }} && {{ python }} -m haven.cli list-commits --repo-path ../.. --base-branch HEAD

# Generate diff files for all commits on current branch
cli-generate:
    cd {{ api_dir }} && {{ python }} -m haven.cli generate --repo-path ../.. --base-branch HEAD --verbose

# Generate diff files to specific output directory
cli-generate-to output_dir:
    cd {{ api_dir }} && {{ python }} -m haven.cli generate --repo-path ../.. --base-branch HEAD --output-dir {{ output_dir }} --verbose

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
    @echo "Python: $(cd {{ api_dir }} && {{ python }} --version)"
    @echo "Environment: {{ api_dir }}/.venv"
    @echo "Working directory: $(pwd)"
    @cd {{ api_dir }} && {{ python }} -m pip list | grep -E "(fastapi|sqlalchemy|strawberry|pydantic)"

# Full CI simulation
ci: clean bootstrap check docs
    @echo "✅ All CI checks passed!"

# Run CI for Python only
ci-python: clean bootstrap-python check docs
    @echo "✅ Python CI checks passed!"

# Build all applications
build: build-api build-web
    @echo "✅ All applications built!"

# Build API (placeholder)
build-api:
    @echo "📦 API build (Docker image)"
    @echo "Run 'just docker-build' to build API Docker image"

# Build Web application
build-web:
    cd {{ web_dir }} && npm run build
    @echo "✅ Web application built to {{ web_dir }}/dist"