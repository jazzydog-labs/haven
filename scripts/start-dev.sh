#!/bin/bash
# Start Haven development environment with proxy on port 80

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🚀 Starting Haven Development Environment"
echo "========================================"
echo ""

# Check if backend is running
if ! curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo "⚠️  Backend not running. Starting it..."
    cd "$PROJECT_ROOT" && just docker::up-d
    
    echo -n "⏳ Waiting for backend to start"
    while ! curl -s http://localhost:8080/health > /dev/null 2>&1; do
        echo -n "."
        sleep 1
    done
    echo " ✅"
else
    echo "✅ Backend already running"
fi

# Check if frontend is running
if ! curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "⚠️  Frontend not running. Starting it..."
    cd "$PROJECT_ROOT/apps/web" && npm run dev > /tmp/haven-frontend.log 2>&1 & echo $! > /tmp/haven-frontend.pid
    
    echo -n "⏳ Waiting for frontend to start"
    while ! curl -s http://localhost:3000 > /dev/null 2>&1; do
        echo -n "."
        sleep 1
    done
    echo " ✅"
else
    echo "✅ Frontend already running"
fi

echo ""
echo "🔐 Starting Caddy proxy on port 80..."
echo "📝 You'll be prompted for your sudo password"
echo ""

# Start Caddy on port 80
cd "$PROJECT_ROOT" && sudo caddy run --config Caddyfile.http80