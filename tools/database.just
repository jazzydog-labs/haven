# Database operations module
# Access these commands with: just database::<command>

import '../.just/common.just'

# Show help for database module
[private]
help:
    @echo "🗄️  Database Commands"
    @echo ""
    @echo "  database::up        Start PostgreSQL"
    @echo "  database::down      Stop database"
    @echo "  database::migrate   Run migrations"
    @echo "  database::console   Database console"
    @echo "  database::reset     Reset database"
    @echo ""

# Start PostgreSQL
up:
    docker compose up -d postgres
    @echo "⏳ Waiting for PostgreSQL to be ready..."
    @sleep 3
    @just _success "PostgreSQL is running"

# Stop database
down:
    docker compose down

# Reset database (removes all data)
reset:
    docker compose down -v
    docker compose up -d postgres
    @sleep 3
    @just _success "Database reset complete"

# Run migrations
migrate:
    cd {{ API_DIR }} && {{ PYTHON }} -m alembic upgrade head

# Create a new migration
make message:
    cd {{ API_DIR }} && {{ PYTHON }} -m alembic revision --autogenerate -m "{{ message }}"

# Show migration history
history:
    cd {{ API_DIR }} && {{ PYTHON }} -m alembic history --verbose

# Show current migration
current:
    cd {{ API_DIR }} && {{ PYTHON }} -m alembic current

# Downgrade database
downgrade steps="1":
    cd {{ API_DIR }} && {{ PYTHON }} -m alembic downgrade -{{ steps }}

# Database console
console:
    docker compose exec postgres psql -U haven -d haven

# Run migrations in Docker
migrate-docker:
    docker compose exec api alembic upgrade head

# Create migration in Docker
make-docker message:
    docker compose exec api alembic revision --autogenerate -m "{{ message }}"

# Database console via Docker
console-docker:
    docker compose exec postgres psql -U haven -d haven