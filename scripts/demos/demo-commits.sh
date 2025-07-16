#!/bin/bash
set -e

# Demo: Start server and view all commits with diffs in browser
# This script starts the API server if needed and runs the diff generation demo

API_DIR="${1:-apps/api}"
PYTHON_CMD="${2:-.venv/bin/python}"

echo "🔍 Starting commit diff viewer in browser"
echo "This will start the server and open all commits with diffs in your browser"
echo ""

# Start server in background if not running
if ! curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo "🚀 Starting server in background..."
    cd "$API_DIR" && $PYTHON_CMD -m haven.main &
    SERVER_PID=$!
    echo "⏳ Waiting for server to be ready..."
    sleep 5
    
    # Wait for server to be ready
    for i in {1..30}; do
        if curl -s http://localhost:8080/health > /dev/null 2>&1; then
            echo "✅ Server is ready!"
            break
        fi
        sleep 1
    done
    
    if ! curl -s http://localhost:8080/health > /dev/null 2>&1; then
        echo "❌ Server failed to start properly"
        exit 1
    fi
else
    echo "✅ Server is already running"
    SERVER_PID=""
fi

# Run the demo
echo "🎯 Running diff generation demo..."
cd "$API_DIR" && $PYTHON_CMD scripts/demo-diff-generation.py

# Keep server running for viewing
echo "🌐 Server running at http://localhost:8080"
echo "Press Ctrl+C to stop the server"

if [ ! -z "$SERVER_PID" ]; then
    wait $SERVER_PID
fi