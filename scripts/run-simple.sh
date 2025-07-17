#!/bin/bash
# Run Haven without proxy (direct access on ports 3000/8080)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🚀 Starting Haven (Simple Mode - No Proxy)"
echo "========================================"
echo ""

# Start backend
cd "$PROJECT_ROOT" && just docker::up-d

# Wait for backend
echo -n "⏳ Waiting for backend to start"
while ! curl -s http://localhost:8080/health > /dev/null 2>&1; do
    echo -n "."
    sleep 1
done
echo " ✅"

# Start frontend
cd "$PROJECT_ROOT/apps/web" && npm run dev > /tmp/haven-frontend.log 2>&1 & echo $! > /tmp/haven-frontend.pid

# Wait for frontend
echo -n "⏳ Waiting for frontend to start"
while ! curl -s http://localhost:3000 > /dev/null 2>&1; do
    echo -n "."
    sleep 1
done
echo " ✅"

echo ""
echo "🎉 Haven is running!"
echo "=================="
echo ""
echo "📱 Access your application at:"
echo "  🌐 Frontend: http://localhost:3000"
echo "  📚 API:      http://localhost:8080"
echo "  📊 Swagger:  http://localhost:8080/docs"
echo "  🔮 GraphQL:  http://localhost:8080/graphql"
echo ""
echo "🛑 To stop: just stop"