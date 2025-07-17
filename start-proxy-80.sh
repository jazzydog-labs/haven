#!/bin/bash
# Start Haven proxy on port 80 (requires sudo)

echo "🚀 Starting Haven services..."
echo "================================"

# Check if backend is running
if ! curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo "⚠️  Backend not running. Starting it..."
    just docker::up-d
    
    # Wait for backend
    echo -n "⏳ Waiting for backend to start"
    while ! curl -s http://localhost:8080/health > /dev/null 2>&1; do
        echo -n "."
        sleep 1
    done
    echo " ✅"
fi

# Check if frontend is running
if ! curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "⚠️  Frontend not running. Starting it..."
    cd apps/web && npm run dev > /tmp/haven-frontend.log 2>&1 &
    
    # Wait for frontend
    echo -n "⏳ Waiting for frontend to start"
    while ! curl -s http://localhost:3000 > /dev/null 2>&1; do
        echo -n "."
        sleep 1
    done
    echo " ✅"
fi

echo ""
echo "🔐 Starting Caddy proxy on port 80..."
echo "📝 You'll be prompted for your sudo password"
echo ""

# Start Caddy on port 80
sudo caddy run --config Caddyfile.http80