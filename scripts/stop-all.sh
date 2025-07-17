#!/bin/bash
# Stop all Haven services

echo "🛑 Stopping all Haven services..."

# Stop Caddy
if [ -f /tmp/haven-caddy.pid ]; then
    PID=$(cat /tmp/haven-caddy.pid)
    kill $PID 2>/dev/null || true
    rm -f /tmp/haven-caddy.pid
    echo "✅ Caddy proxy stopped"
fi

# Kill any remaining Caddy processes
pkill -f caddy 2>/dev/null || true

# Stop frontend from PID file
if [ -f /tmp/haven-frontend.pid ]; then
    PID=$(cat /tmp/haven-frontend.pid)
    kill $PID 2>/dev/null || true
    rm -f /tmp/haven-frontend.pid
    echo "✅ Frontend stopped (from PID file)"
fi

# Kill any remaining frontend processes
pkill -f "npm run dev" 2>/dev/null || true
pkill -f "vite --host" 2>/dev/null || true
echo "✅ All frontend processes stopped"

# Stop backend
docker compose down > /dev/null 2>&1
echo "✅ Backend stopped"

# Clean up logs
rm -f /tmp/haven-frontend.log /tmp/haven-caddy.log

echo "🏁 All services stopped"