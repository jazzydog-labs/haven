# Testing operations module
# Access these commands with: just test::<command>

import '../.just/common.just'

# Show help for testing module
[private]
help:
    @echo "🧪 Testing Commands"
    @echo ""
    @echo "  test::all          Run all tests"
    @echo "  test::python       Run Python tests"
    @echo "  test::web          Run web tests"
    @echo "  test::fast         Run fast tests only"
    @echo "  test::watch        Run tests in watch mode"
    @echo "  test::coverage     Run with coverage report"
    @echo ""

# Run all tests
all:
    @just _section "Running all tests"
    @just test::python
    @just test::web

# Run Python tests
python:
    cd {{ API_DIR }} && {{ PYTHON }} -m pytest

# Run web tests
web:
    cd {{ WEB_DIR }} && npm test

# Run fast tests only
fast:
    cd {{ API_DIR }} && {{ PYTHON }} -m pytest -m "not slow"

# Run tests in watch mode
watch:
    cd {{ API_DIR }} && {{ PYTHON }} -m pytest-watch

# Run tests with coverage
coverage:
    cd {{ API_DIR }} && {{ PYTHON }} -m pytest --cov=haven --cov-report=html --cov-report=term

# Run specific test file
file file:
    cd {{ API_DIR }} && {{ PYTHON }} -m pytest {{ file }}

# Run tests in Docker
docker:
    docker compose run --rm api pytest tests/ --no-cov

# Run tests with coverage in Docker
docker-coverage:
    docker compose run --rm api pytest tests/ --cov=haven --cov-report=html

# Validate all just commands
validate:
    @just _section "Validating all just commands"
    @{{ PROJECT_ROOT }}/.just/test-commands.sh