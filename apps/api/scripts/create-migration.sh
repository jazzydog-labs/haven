#!/bin/bash
# Helper script to create Alembic migrations with proper naming

set -euo pipefail

# Check if message provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <migration message>"
    echo "Example: $0 'add user table'"
    exit 1
fi

MESSAGE="$1"

# Generate timestamp for filename
TIMESTAMP=$(date +%Y%m%d_%H%M)

# Create migration
echo "Creating migration: $MESSAGE"
alembic revision --autogenerate -m "$MESSAGE"

# Find the newly created file and rename it
LATEST_FILE=$(ls -t alembic/versions/*.py | head -n1)
if [ -f "$LATEST_FILE" ]; then
    # Extract revision ID from file
    REV_ID=$(grep "revision = " "$LATEST_FILE" | cut -d"'" -f2 | cut -c1-12)
    
    # Create new filename with timestamp
    SLUG=$(echo "$MESSAGE" | tr '[:upper:]' '[:lower:]' | tr ' ' '_' | tr -cd '[:alnum:]_')
    NEW_NAME="alembic/versions/${TIMESTAMP}_${SLUG}.py"
    
    # Rename file
    mv "$LATEST_FILE" "$NEW_NAME"
    echo "Migration created: $NEW_NAME"
else
    echo "Error: Could not find migration file"
    exit 1
fi