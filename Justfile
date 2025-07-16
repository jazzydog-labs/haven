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

# Run everything (frontend + backend)
run: run-all

# Run all services (recommended)
run-all:
    @echo "🚀 Starting Haven Development Environment..."
    @echo "==========================================="
    @echo ""
    
    # Start backend services in background
    @just docker::up-d > /dev/null 2>&1
    
    # Wait for backend to be ready
    @echo "⏳ Waiting for backend services to start..."
    @while ! curl -s http://localhost:8080/health > /dev/null 2>&1; do \
        printf "."; \
        sleep 0.3; \
    done
    @echo ""
    
    @just _success "Backend services ready!"
    @echo ""
    
    # Start frontend in background
    @echo "🎨 Starting frontend development server..."
    @cd {{ WEB_DIR }} && npm run dev > /tmp/haven-frontend.log 2>&1 & echo $$! > /tmp/haven-frontend.pid
    
    # Wait for frontend
    @echo "⏳ Waiting for frontend to start..."
    @while ! curl -s http://localhost:3000 > /dev/null 2>&1; do \
        printf "."; \
        sleep 0.3; \
    done
    @echo ""
    
    @just _success "Frontend ready!"
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
    @echo "  Backend:  just docker::logs api"
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
    @just docker::down > /dev/null 2>&1
    @echo "✅ Backend stopped"
    
    # Clean up
    @rm -f /tmp/haven-frontend.log
    
    @echo "🏁 All services stopped"

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
    @just docker::up-d > /dev/null 2>&1
    
    # Wait for backend to be ready
    @echo "⏳ Waiting for backend services to start..."
    @while ! curl -s http://localhost:8080/health > /dev/null 2>&1; do \
        printf "."; \
        sleep 0.3; \
    done
    @echo ""
    @just _success "Backend services ready!"
    @echo ""
    
    # Start frontend in background
    @echo "🎨 Starting frontend development server..."
    @cd {{ WEB_DIR }} && npm run dev > /tmp/haven-frontend.log 2>&1 & echo $$! > /tmp/haven-frontend.pid
    
    # Wait for frontend
    @echo "⏳ Waiting for frontend to start..."
    @while ! curl -s http://localhost:3000 > /dev/null 2>&1; do \
        printf "."; \
        sleep 0.3; \
    done
    @echo ""
    @just _success "Frontend ready!"
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
    @echo "  Backend:  just docker::logs api"
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
    @just docker::down > /dev/null 2>&1
    @echo "✅ Backend stopped"
    
    # Clean up
    @rm -f /tmp/haven-frontend.log /tmp/haven-caddy.log
    
    @echo "🏁 All services stopped"

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

# Show current environment info
info:
    @just _section "Haven Environment Info"
    @echo "Working directory: $(pwd)"
    @echo ""
    @echo "=== API Info ==="
    @cd {{ API_DIR }} && just info
    @echo ""
    @echo "=== Web Info ==="
    @cd {{ WEB_DIR }} && just info

# Validate all commands
validate:
    @just testing::validate

# === Legacy command mappings (for backwards compatibility) ===

# Run API server (standalone)
run-api:
    @just _warn "Use 'just api::dev' instead"
    @just api::dev

# Run Web development server (standalone)
run-web:
    @just _warn "Use 'just web::dev' instead"
    @just web::dev

# Docker commands (mapped to docker module)
run-docker:
    @just _warn "Use 'just docker::up' instead"
    @just docker::up

run-docker-d:
    @just _warn "Use 'just docker::up-d' instead"
    @just docker::up-d

stop-docker:
    @just _warn "Use 'just docker::down' instead"
    @just docker::down

logs-docker service="":
    @just _warn "Use 'just docker::logs {{ service }}' instead"
    @just docker::logs {{ service }}

# Database commands (mapped to database module)
db-up:
    @just _warn "Use 'just database::up' instead"
    @just database::up

db-migrate:
    @just _warn "Use 'just database::migrate' instead"
    @just database::migrate

db-console:
    @just _warn "Use 'just database::console' instead"
    @just database::console

db-reset:
    @just _warn "Use 'just database::reset' instead"
    @just database::reset

# Test commands (mapped to testing module)
test:
    @just _warn "Use 'just testing::all' instead"
    @just testing::all

test-python:
    @just _warn "Use 'just testing::python' instead"
    @just testing::python

test-web:
    @just _warn "Use 'just testing::web' instead"
    @just testing::web

# Package-specific commands
lint-python:
    @just _warn "Use 'just api::lint' instead"
    @just api::lint

lint-web:
    @just _warn "Use 'just web::lint' instead"
    @just web::lint

# Aliases for common commands
start: run-all
stop: stop-all
down: stop-docker