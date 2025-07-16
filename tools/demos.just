# Demo commands module
# Access these commands with: just demos::<command>

import '../.just/common.just'

# Show available demos
[private]
help:
    @echo "🎯 Demo Commands"
    @echo ""
    @echo "  demos::health       Test health endpoints"
    @echo "  demos::api          Show REST API operations"
    @echo "  demos::graphql      Demonstrate GraphQL"
    @echo "  demos::docker       Test containerization"
    @echo "  demos::all          Run all demos"
    @echo ""

# Demo: Health check endpoints
health:
    @just _section "Testing health endpoints"
    @echo "REST Health:"
    curl -s http://localhost:8080/health | jq '.' || just _error "API not running - start with: just run"
    @echo ""
    @echo "GraphQL Health:"
    curl -s -X POST http://localhost:8080/graphql \
        -H "Content-Type: application/json" \
        -d '{"query": "{ health { status message timestamp } }"}' | jq '.' || just _error "GraphQL not available"

# Demo: REST API CRUD operations
api:
    @just _section "Testing REST API endpoints"
    @echo "1. Create a record:"
    curl -s -X POST http://localhost:8080/api/v1/records \
        -H "Content-Type: application/json" \
        -d '{"name": "Demo Record", "description": "Created by demo"}' | jq '.' || just _error "API not running"
    @echo ""
    @echo "2. List all records:"
    curl -s http://localhost:8080/api/v1/records | jq '.' || just _error "API not running"
    @echo ""
    @just _info "Full API docs at: http://localhost:8080/docs"

# Demo: GraphQL operations
graphql:
    @just _section "Testing GraphQL operations"
    @echo "1. Query all records:"
    curl -s -X POST http://localhost:8080/graphql \
        -H "Content-Type: application/json" \
        -d '{"query": "{ records { id name description createdAt } }"}' | jq '.' || just _error "GraphQL not available"
    @echo ""
    @echo "2. Create via mutation:"
    curl -s -X POST http://localhost:8080/graphql \
        -H "Content-Type: application/json" \
        -d '{"query": "mutation { createRecord(input: {name: \"GraphQL Demo\", description: \"Created via GraphQL\"}) { id name } }"}' | jq '.' || just _error "GraphQL not available"
    @echo ""
    @just _info "Interactive GraphQL at: http://localhost:8080/graphql"

# Demo: Docker containerization
docker:
    @just _section "Testing Docker setup"
    @echo "Container status:"
    docker compose ps
    @echo ""
    @echo "Testing containerized API:"
    docker compose exec api curl -s http://localhost:8080/health | jq '.' || just _error "Container not running"
    @echo ""
    @echo "Database connection:"
    docker compose exec postgres pg_isready || just _error "PostgreSQL not ready"

# Demo: Migration strategies
migrations:
    @just _section "Demonstrating migration strategies"
    @echo "Current migration status:"
    just database::current || just _error "Database not running"
    @echo ""
    @echo "Available migration methods:"
    @echo "1. Host-based:     just database::migrate"
    @echo "2. Exec method:    just database::migrate-docker"
    @echo "3. One-shot:       docker compose run --rm api alembic upgrade head"

# Demo: TTR System
ttr:
    @just _section "TTR (Task, Todo, Review) System Demo"
    @echo "Prerequisites:"
    @echo "  - Database running: just database::up"
    @echo "  - Migrations applied: just database::migrate"
    @echo ""
    @echo "Running TTR system demo..."
    cd {{ API_DIR }} && {{ PYTHON }} -c "import asyncio; from haven.demo.ttr_demo import demo_ttr_system; asyncio.run(demo_ttr_system())"

# Demo: Frontend-Backend Sync
sync:
    @just _section "Frontend-Backend Sync Workflow"
    ./scripts/demo-sync-workflow.sh

# Demo: HTTPS Setup
https:
    @just _section "HTTPS Setup Demo"
    ./scripts/demo-https.sh

# Demo: CORS configuration
cors:
    @just _section "Testing CORS configuration"
    @echo "Testing cross-origin request:"
    curl -s -X OPTIONS http://localhost:8080/api/v1/records \
        -H "Origin: http://localhost:3000" \
        -H "Access-Control-Request-Method: GET" \
        -I | grep -i "access-control" || just _error "CORS headers not found"

# Run all demos
all:
    @just _section "Running all demos"
    @just demos::health
    @echo ""
    @just demos::api
    @echo ""
    @just demos::graphql
    @echo ""
    @just demos::docker
    @echo ""
    @just _success "All demos complete!"