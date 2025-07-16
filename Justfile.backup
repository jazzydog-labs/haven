# Haven Development Justfile - Main Orchestrator
# Run `just --list` to see all available commands

# Import common variables and settings
import 'justfile.common'

# Import module-specific justfiles
import 'justfile.database'
import 'justfile.docker'
import 'justfile.demos'

# Default recipe shows available commands
default:
    @just --list

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

# Run everything in development mode with hot-reload
run: run-all

# Run all services (recommended)
run-all:
    @echo "🚀 Starting Haven Development Environment..."
    @echo "==========================================="
    @echo ""
    
    # Start backend services in background
    @just run-docker-d > /dev/null 2>&1
    
    # Wait for backend to be ready
    @echo "⏳ Waiting for backend services to start..."
    @while ! curl -s http://localhost:8080/health > /dev/null 2>&1; do \
        printf "."; \
        sleep 0.3; \
    done
    @echo ""
    
    @echo "✅ Backend services ready!"
    @echo ""
    
    # Start frontend in background
    @echo "🎨 Starting frontend development server..."
    @cd {{ web_dir }} && npm run dev > /tmp/haven-frontend.log 2>&1 & echo $$! > /tmp/haven-frontend.pid
    
    # Wait for frontend
    @echo "⏳ Waiting for frontend to start..."
    @while ! curl -s http://localhost:3000 > /dev/null 2>&1; do \
        printf "."; \
        sleep 0.3; \
    done
    @echo ""
    
    @echo "✅ Frontend ready!"
    @echo ""
    @echo "======================================"
    @echo "🎉 Haven is running!"
    @echo "======================================"
    @echo ""
    @echo "📱 Access your application at:"
    @echo ""
    @echo "  🌐 Frontend:    http://localhost:3000"
    @echo "  📊 Records:     http://localhost:3000  (Records section)"
    @echo "  📚 API Docs:    http://localhost:8080/docs"
    @echo "  🔮 GraphQL:     http://localhost:8080/graphql"
    @echo "  ❤️  Health:     http://localhost:8080/health"
    @echo ""
    @echo "🌐 Or use local domains (run 'just setup-hosts' first):"
    @echo "  🌐 Frontend:    http://web.haven.local:3000"
    @echo "  📚 API:         http://api.haven.local:8080"
    @echo "  🎉 Better:      Run 'just run-proxy' for clean URLs"
    @echo ""
    @echo "🔥 Hot-reload enabled for both frontend and backend!"
    @echo ""
    @echo "📝 Logs:"
    @echo "  Backend:  just logs-docker api"
    @echo "  Frontend: tail -f /tmp/haven-frontend.log"
    @echo ""
    @echo "🛑 To stop everything: just stop-all"
    @echo ""
    @echo "Press Ctrl+C to exit (services will continue running)"
    @echo ""
    
    # Keep running to show the info
    @while true; do sleep 60; done

# Stop all services
stop-all:
    @echo "🛑 Stopping all Haven services..."
    
    # Stop frontend if running
    @if [ -f /tmp/haven-frontend.pid ]; then \
        PID=`cat /tmp/haven-frontend.pid`; \
        kill $$PID 2>/dev/null || true; \
        rm -f /tmp/haven-frontend.pid; \
        echo "✅ Frontend stopped"; \
    fi
    
    # Stop backend
    @just stop-docker > /dev/null 2>&1
    @echo "✅ Backend stopped"
    
    # Clean up
    @rm -f /tmp/haven-frontend.log
    
    @echo "🏁 All services stopped"

# Run API server (standalone)
run-api:
    cd {{ api_dir }} && just run

# Run Web development server (standalone)
run-web:
    cd {{ web_dir }} && just run

# Quick start (alias)
start: run-all

# Quick stop (alias)
stop: stop-all

# Run with specific environment
run-env env="local":
    cd {{ api_dir }} && just run-env {{ env }}

# Quality checks for all code
lint: lint-python lint-web
    @echo "✅ All linting passed!"

# Python linting
lint-python:
    cd {{ api_dir }} && just lint

# Web linting
lint-web:
    cd {{ web_dir }} && just lint

# Fix linting issues
lint-fix: lint-fix-python lint-fix-web
    @echo "✅ All linting issues fixed!"

lint-fix-python:
    cd {{ api_dir }} && just lint-fix

lint-fix-web:
    cd {{ web_dir }} && just lint-fix

# Format all code
format: format-python format-web
    @echo "✅ All code formatted!"

format-python:
    cd {{ api_dir }} && just format

format-web:
    cd {{ web_dir }} && just format

# Type checking
type: type-python type-web
    @echo "✅ All type checking passed!"

type-python:
    cd {{ api_dir }} && just type

type-web:
    cd {{ web_dir }} && just type

# Sync frontend types with backend API
sync-types:
    @echo "🔄 Syncing frontend types with backend..."
    ./scripts/sync-frontend-backend.sh

# Check for API breaking changes
check-api-compat:
    @echo "🔍 Checking API compatibility..."
    @if [ -f {{ web_dir }}/src/types/openapi.prev.json ]; then \
        diff -u {{ web_dir }}/src/types/openapi.prev.json {{ web_dir }}/src/types/openapi.json || echo "⚠️  API changes detected"; \
    else \
        echo "No previous API spec found for comparison"; \
    fi

# Generate CRUD components for a model
generate-frontend-crud model:
    @echo "🏗️  Generating CRUD components for {{ model }}..."
    @echo "TODO: Implement CRUD component generation"
    @echo "- Create components/{{ model }}/{{ model }}List.tsx"
    @echo "- Create components/{{ model }}/{{ model }}Form.tsx"
    @echo "- Create components/{{ model }}/{{ model }}Detail.tsx"
    @echo "- Create hooks/use{{ model }}.ts"
    @echo "- Create services/api/{{ model }}.ts"

# Run all quality checks
check: lint type test-fast

# Run Python quality checks only
check-python:
    cd {{ api_dir }} && just check

# Run Web quality checks only  
check-web:
    cd {{ web_dir }} && just check

# Run all tests
test: test-python test-web
    @echo "✅ All tests passed!"

# Python testing
test-python:
    cd {{ api_dir }} && just test

# Web testing
test-web:
    cd {{ web_dir }} && just test

test-fast: test-fast-python
    @echo "✅ Fast tests passed!"

test-fast-python:
    cd {{ api_dir }} && just test-fast

# Coverage testing
test-cov: test-cov-python
    @echo "✅ Coverage report generated!"

test-cov-python:
    cd {{ api_dir }} && just test-cov

# Watch mode testing
test-watch: test-watch-python

test-watch-python:
    cd {{ api_dir }} && just test-watch

# Run specific test file
test-file file:
    cd {{ api_dir }} && just test-file {{ file }}

# Documentation
docs:
    cd {{ api_dir }} && {{ python }} -m mkdocs build --config-file ../../mkdocs.yml --site-dir ../../site

docs-serve:
    cd {{ api_dir }} && {{ python }} -m mkdocs serve --config-file ../../mkdocs.yml --dev-addr localhost:8001

docs-deploy:
    cd {{ api_dir }} && {{ python }} -m mkdocs gh-deploy --config-file ../../mkdocs.yml --force

# Development utilities
shell:
    cd {{ api_dir }} && just shell

# Show logs
logs:
    docker compose logs -f

# Clean up generated files
clean: clean-python clean-web
    rm -rf .tmp/
    rm -rf apps/api/diff-out*/ apps/api/diff-demo*/
    rm -f server.log
    @echo "✅ All cleaned!"

clean-python:
    cd {{ api_dir }} && just clean

clean-web:
    cd {{ web_dir }} && just clean

# Pre-commit setup
pre-commit-install:
    pre-commit install

pre-commit-run:
    pre-commit run --all-files

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
    @echo "=== Monorepo Info ==="
    @echo "Working directory: $(pwd)"
    @echo ""
    @echo "=== API Info ==="
    @cd {{ api_dir }} && just info
    @echo ""
    @echo "=== Web Info ==="
    @cd {{ web_dir }} && just info

# Full CI simulation
ci: clean bootstrap check docs
    @echo "✅ All CI checks passed!"

# Run CI for Python only
ci-python: clean bootstrap-python check-python docs
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
    cd {{ web_dir }} && just build

# Setup local HTTPS development
setup-https:
    @echo "🔐 Setting up local HTTPS..."
    ./scripts/setup-https.sh

# Run with HTTPS using Caddy
run-https:
    docker compose -f docker-compose.yml -f docker-compose.https.yml up

# Run with HTTPS in background
run-https-d:
    docker compose -f docker-compose.yml -f docker-compose.https.yml up -d
    @echo "🔒 HTTPS services running:"
    @echo "  - https://haven.local (web app)"
    @echo "  - https://api.haven.local (API)"
    @echo "  - https://api.haven.local/docs (Swagger)"

# Stop HTTPS services
stop-https:
    docker compose -f docker-compose.yml -f docker-compose.https.yml down

# Setup local hosts entries
setup-hosts:
    @echo "🌐 Setting up local domain mappings"
    @sudo ./scripts/setup-hosts.sh

# Remove local hosts entries
remove-hosts:
    @echo "🧹 Removing Haven domain mappings"
    @sudo ./scripts/setup-hosts.sh --remove

# Run with local reverse proxy (includes hosts setup)
run-proxy: setup-hosts
    @echo "🚀 Starting Haven with reverse proxy..."
    @echo "==========================================="
    @echo ""
    
    # Start backend services in background
    @just run-docker-d > /dev/null 2>&1
    
    # Wait for backend to be ready
    @echo "⏳ Waiting for backend services to start..."
    @while ! curl -s http://localhost:8080/health > /dev/null 2>&1; do \
        printf "."; \
        sleep 0.3; \
    done
    @echo ""
    @echo "✅ Backend services ready!"
    @echo ""
    
    # Start frontend in background
    @echo "🎨 Starting frontend development server..."
    @cd {{ web_dir }} && npm run dev > /tmp/haven-frontend.log 2>&1 & echo $$! > /tmp/haven-frontend.pid
    
    # Wait for frontend
    @echo "⏳ Waiting for frontend to start..."
    @while ! curl -s http://localhost:3000 > /dev/null 2>&1; do \
        printf "."; \
        sleep 0.3; \
    done
    @echo ""
    @echo "✅ Frontend ready!"
    @echo ""
    
    # Start Caddy proxy
    @echo "🔐 Starting Caddy reverse proxy..."
    @caddy run --config ./Caddyfile --adapter caddyfile > /tmp/haven-caddy.log 2>&1 & echo $$! > /tmp/haven-caddy.pid
    
    # Wait for Caddy
    @sleep 2
    
    @echo ""
    @echo "======================================"
    @echo "🎉 Haven is running with reverse proxy!"
    @echo "======================================"
    @echo ""
    @echo "📱 Access your application at:"
    @echo ""
    @echo "  🌐 Main:        http://haven.local"
    @echo "  🌐 Frontend:    http://web.haven.local"
    @echo "  📚 API:         http://api.haven.local"
    @echo "  📊 Swagger:     http://api.haven.local/docs"
    @echo "  🔮 GraphQL:     http://api.haven.local/graphql"
    @echo "  ❤️  Health:     http://api.haven.local/health"
    @echo ""
    @echo "🔥 Hot-reload enabled for both frontend and backend!"
    @echo "🔒 HTTPS available at https://haven.local (if certificates are set up)"
    @echo ""
    @echo "📝 Logs:"
    @echo "  Backend:  just logs-docker api"
    @echo "  Frontend: tail -f /tmp/haven-frontend.log"
    @echo "  Proxy:    tail -f /tmp/haven-caddy.log"
    @echo ""
    @echo "🛑 To stop everything: just stop-proxy"
    @echo ""
    @echo "Press Ctrl+C to exit (services will continue running)"
    @echo ""
    
    # Keep running to show the info
    @while true; do sleep 60; done

# Stop proxy and all services
stop-proxy:
    @echo "🛑 Stopping all Haven services..."
    
    # Stop Caddy if running
    @if [ -f /tmp/haven-caddy.pid ]; then \
        PID=`cat /tmp/haven-caddy.pid`; \
        kill $$PID 2>/dev/null || true; \
        rm -f /tmp/haven-caddy.pid; \
        echo "✅ Caddy proxy stopped"; \
    fi
    
    # Stop frontend if running
    @if [ -f /tmp/haven-frontend.pid ]; then \
        PID=`cat /tmp/haven-frontend.pid`; \
        kill $$PID 2>/dev/null || true; \
        rm -f /tmp/haven-frontend.pid; \
        echo "✅ Frontend stopped"; \
    fi
    
    # Stop backend
    @just stop-docker > /dev/null 2>&1
    @echo "✅ Backend stopped"
    
    # Clean up
    @rm -f /tmp/haven-frontend.log /tmp/haven-caddy.log
    
    @echo "🏁 All services stopped"