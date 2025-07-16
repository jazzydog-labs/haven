#!/bin/bash

echo "🧪 Testing Complete Haven Setup"
echo "==============================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

test_url() {
    local url=$1
    local name=$2
    
    if curl -s "$url" > /dev/null 2>&1; then
        echo -e "  ✅ ${GREEN}$name${NC}: $url"
        return 0
    else
        echo -e "  ❌ ${RED}$name${NC}: $url"
        return 1
    fi
}

# Test 1: Domain resolution
echo "1. Testing domain resolution..."
if ping -c 1 web.haven.local > /dev/null 2>&1; then
    echo -e "  ✅ ${GREEN}Domains resolve to localhost${NC}"
else
    echo -e "  ❌ ${RED}Domains do not resolve${NC}"
    echo "  💡 Run: just setup-hosts"
fi
echo ""

# Test 2: Direct service access
echo "2. Testing direct service access..."
test_url "http://localhost:3000" "Frontend (direct)"
test_url "http://localhost:8080/health" "Backend (direct)"
echo ""

# Test 3: Domain access with ports
echo "3. Testing domain access with ports..."
test_url "http://web.haven.local:3000" "Frontend (domain+port)"
test_url "http://api.haven.local:8080/health" "Backend (domain+port)"
echo ""

# Test 4: Reverse proxy access
echo "4. Testing reverse proxy access..."
test_url "http://web.haven.local:8000" "Frontend (proxy)"
test_url "http://haven.local:8000" "Main domain (proxy)"
test_url "http://api.haven.local:8000/health" "Backend (proxy)"
test_url "http://api.haven.local:8000/docs" "API Docs (proxy)"
echo ""

# Test 5: API endpoints
echo "5. Testing API endpoints..."
if curl -s "http://api.haven.local:8000/health" | grep -q "healthy"; then
    echo -e "  ✅ ${GREEN}Health endpoint working${NC}"
else
    echo -e "  ❌ ${RED}Health endpoint not working${NC}"
fi

if curl -s "http://api.haven.local:8000/docs" | grep -q "swagger"; then
    echo -e "  ✅ ${GREEN}Swagger docs working${NC}"
else
    echo -e "  ❌ ${RED}Swagger docs not working${NC}"
fi

if curl -s "http://api.haven.local:8000/graphql" | grep -q "GraphQL"; then
    echo -e "  ✅ ${GREEN}GraphQL endpoint working${NC}"
else
    echo -e "  ❌ ${RED}GraphQL endpoint not working${NC}"
fi
echo ""

# Test 6: Browser simulation
echo "6. Testing browser compatibility..."
if curl -s -H "User-Agent: Mozilla/5.0" "http://web.haven.local:8000" | grep -q "html"; then
    echo -e "  ✅ ${GREEN}Frontend serves HTML${NC}"
else
    echo -e "  ❌ ${RED}Frontend HTML not served${NC}"
fi
echo ""

echo "🎯 Summary:"
echo "==========="
echo ""
echo "✅ Working URLs for browser testing:"
echo "  • Frontend: http://web.haven.local:8000"
echo "  • Main App: http://haven.local:8000"
echo "  • API Health: http://api.haven.local:8000/health"
echo "  • API Docs: http://api.haven.local:8000/docs"
echo "  • GraphQL: http://api.haven.local:8000/graphql"
echo ""
echo "🔧 Commands:"
echo "  • Start everything: just run-proxy"
echo "  • Stop everything: just stop-all"
echo "  • Remove domains: just remove-hosts"
echo ""
echo "🎉 You should now be able to access http://web.haven.local:8000 in your browser!"