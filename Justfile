# Haven Development Commands
# Type 'just' to see all available commands

# Import common utilities
import '.just/common.just'

# Import tool modules
mod docker 'tools/docker.just'
mod database 'tools/database.just'
mod testing 'tools/testing.just'
mod demos 'tools/demos.just'

# Package commands
mod api 'apps/api/justfile'
mod web 'apps/web/justfile'

# Show interactive command picker (default)
[private]
default:
    @just --choose

# Show beautiful help
help:
    @.just/help.sh

# Bootstrap entire monorepo
bootstrap: bootstrap-python bootstrap-web
    @just _success "Monorepo bootstrap complete!"

# Create Python virtual environment
bootstrap-python:
    cd {{ API_DIR }} && python3.12 -m venv .venv
    cd {{ API_DIR }} && .venv/bin/pip install --upgrade pip
    cd {{ API_DIR }} && .venv/bin/pip install -e ".[dev]"
    @just _success "Python environment ready! Run 'source {{ API_DIR }}/.venv/bin/activate' to activate"

# Install Node.js dependencies
bootstrap-web:
    cd {{ WEB_DIR }} && npm install
    @just _success "Web environment ready!"

# 🚀 Main development command - starts everything with proxy on port 80
run: _check-hosts
    @./scripts/start-dev.sh

# Run without proxy (simple mode)
run-simple:
    @./scripts/run-simple.sh

# Stop all services
stop:
    @./scripts/stop-all.sh

# Alias for backward compatibility
stop-all: stop

# Setup local hosts entries
setup-hosts:
    @echo "🌐 Setting up local domain mappings"
    @sudo ./scripts/setup-hosts.sh

# Remove local hosts entries
remove-hosts:
    @echo "🧹 Removing Haven domain mappings"
    @sudo ./scripts/setup-hosts.sh --remove

# Check if hosts are configured, set up if needed
[private]
_check-hosts:
    @if ! grep -q "haven.local" /etc/hosts; then \
        echo "🌐 Setting up local domain mappings..."; \
        just setup-hosts; \
    else \
        echo "✅ Local domain mappings already configured"; \
    fi

# Run all quality checks
check: lint type test-fast

# Run linting
lint:
    @just _section "Running linters"
    @just api::lint
    @just web::lint

# Run type checking
type:
    @just _section "Running type checkers"
    @just api::type
    @just web::type

# Run fast tests
test-fast:
    @just testing::fast

# Format all code
format:
    @just _section "Formatting code"
    @just api::format
    @just web::format

# Clean everything
clean:
    @just _section "Cleaning project"
    rm -rf .tmp/
    rm -rf apps/api/diff-out*/ apps/api/diff-demo*/
    rm -f server.log
    @just api::clean
    @just web::clean
    @just _success "All cleaned!"

# Sync frontend types with backend API
sync-types:
    @echo "🔄 Syncing frontend types with backend..."
    ./scripts/sync-frontend-backend.sh

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

# Build for production
build:
    @just api::build
    @just web::build
    @just _success "Production build complete!"

# View logs
logs:
    @echo "Choose which logs to view:"
    @echo "  1) Backend (API)"
    @echo "  2) Frontend"
    @echo "  3) Proxy (Caddy)"
    @echo "  4) All"
    @read -p "Enter choice (1-4): " choice; \
    case $$choice in \
        1) just docker::logs api ;; \
        2) tail -f /tmp/haven-frontend.log ;; \
        3) tail -f /tmp/haven-caddy.log ;; \
        4) echo "Starting all logs..."; \
           just docker::logs api & \
           tail -f /tmp/haven-frontend.log & \
           tail -f /tmp/haven-caddy.log ;; \
        *) echo "Invalid choice" ;; \
    esac

# Interactive shell
shell:
    @just api::shell

# Show status of all services
status:
    @echo "🔍 Checking service status..."
    @echo ""
    @if curl -s http://localhost:8080/health > /dev/null 2>&1; then \
        echo "✅ Backend: Running on http://localhost:8080"; \
    else \
        echo "❌ Backend: Not running"; \
    fi
    @if curl -s http://localhost:3000 > /dev/null 2>&1; then \
        echo "✅ Frontend: Running on http://localhost:3000"; \
    else \
        echo "❌ Frontend: Not running"; \
    fi
    @if curl -s http://haven.local > /dev/null 2>&1; then \
        echo "✅ Proxy: Running on http://haven.local (port 80)"; \
    elif curl -s http://haven.local:9000 > /dev/null 2>&1; then \
        echo "✅ Proxy: Running on http://haven.local:9000"; \
    else \
        echo "❌ Proxy: Not running"; \
    fi

# Quick restart
restart: stop run