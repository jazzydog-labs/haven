#!/bin/bash
set -e

# Demo: Diff Generation API (requires server to be running)
# This script checks if the server is running and executes the diff generation demo

API_DIR="${1:-apps/api}"
PYTHON_CMD="${2:-.venv/bin/python}"

echo "🔍 Diff Generation API Demo"
echo "This demo shows how to use the FastAPI diff generation endpoints"
echo ""

# Check if server is running
if ! curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo "❌ Server is not running. Starting server..."
    echo "   Run 'just run' in another terminal first"
    exit 1
fi

echo "✅ Server is running"
echo "🎯 Running diff generation demo..."

# Run the demo
cd "$API_DIR" && $PYTHON_CMD scripts/demo-diff-generation.py