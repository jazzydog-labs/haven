#!/bin/bash

echo "🧪 Testing Haven domain configuration..."
echo "========================================="
echo ""

# Test direct access with ports
echo "1. Testing direct access with ports:"
echo "   Backend:   http://localhost:8080/health"
echo "   Frontend:  http://localhost:3000"
echo ""

# Test domains with ports
echo "2. Testing domains with ports:"
echo "   Backend:   http://api.haven.local:8080/health"
echo "   Frontend:  http://web.haven.local:3000"
echo ""

# Test backend health endpoint
echo "🔍 Testing backend health endpoint..."
if curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo "   ✅ Backend is running on localhost:8080"
else
    echo "   ❌ Backend is not running on localhost:8080"
    echo "   💡 Start with: just docker::up-d"
fi

# Test frontend
echo "🔍 Testing frontend server..."
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "   ✅ Frontend is running on localhost:3000"
else
    echo "   ❌ Frontend is not running on localhost:3000"
    echo "   💡 Start with: cd apps/web && npm run dev"
fi

# Test domain resolution
echo "🔍 Testing domain resolution..."
if ping -c 1 haven.local > /dev/null 2>&1; then
    echo "   ✅ haven.local resolves to localhost"
else
    echo "   ❌ haven.local does not resolve"
    echo "   💡 Run: just setup-hosts"
fi

echo ""
echo "🌐 Try accessing these URLs in your browser:"
echo "   • http://web.haven.local:3000 (direct frontend)"
echo "   • http://api.haven.local:8080/health (direct backend)"
echo "   • http://api.haven.local:8080/docs (API docs)"
echo ""
echo "🔧 For clean URLs without ports, run: just run-proxy"