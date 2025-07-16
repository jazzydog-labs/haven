#!/bin/bash
# Run Alembic migrations in Docker container

set -e

# Check if we're running inside or outside the container
if [ -f /.dockerenv ]; then
    # Inside container - run migrations directly
    echo "Running migrations inside container..."
    cd /app
    alembic upgrade head
else
    # Outside container - execute in the api container
    echo "Running migrations via docker-compose..."
    docker-compose exec api alembic upgrade head
fi