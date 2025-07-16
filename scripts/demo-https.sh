#!/bin/bash
# Demo script for HTTPS setup

set -e

echo "🔒 HTTPS Development Demo"
echo "========================"
echo ""

# Check if certificates exist
if [ ! -d "certs" ] || [ ! -f "certs/cert.pem" ]; then
    echo "❌ Certificates not found. Please run: just setup-https"
    exit 1
fi

echo "✅ Certificates found"
echo ""

# Show certificate details
echo "📜 Certificate Details:"
openssl x509 -in certs/cert.pem -subject -issuer -dates -noout | sed 's/^/   /'
echo ""

# Check hosts file
echo "🌐 Checking hosts file..."
if grep -q "haven.local" /etc/hosts; then
    echo "✅ Hosts file configured"
else
    echo "⚠️  Hosts file not configured. Add these lines to /etc/hosts:"
    echo "   127.0.0.1    haven.local"
    echo "   127.0.0.1    api.haven.local"
    echo "   127.0.0.1    app.haven.local"
fi
echo ""

# Check if services are running
echo "🐳 Checking services..."
if docker compose ps | grep -q "haven-api.*running"; then
    echo "✅ API service is running"
else
    echo "⚠️  API service not running. Start with: just run-docker-d"
fi
echo ""

# Test HTTPS endpoints
echo "🧪 Testing HTTPS endpoints..."
echo ""

# Function to test endpoint
test_endpoint() {
    local url=$1
    local desc=$2
    
    echo -n "  $desc: "
    if curl -sk --max-time 2 "$url" > /dev/null 2>&1; then
        echo "✅ Accessible"
    else
        echo "❌ Not accessible"
    fi
}

# Test different configurations
echo "Option 1: Direct HTTPS (if running with certificates)"
test_endpoint "https://localhost:8443/health" "API Health"
echo ""

echo "Option 2: Via Caddy reverse proxy (if running)"
test_endpoint "https://api.haven.local/health" "API via Caddy"
test_endpoint "https://haven.local" "Web App via Caddy"
echo ""

echo "Option 3: Standard HTTP (current setup)"
test_endpoint "http://localhost:8080/health" "API Health (HTTP)"
test_endpoint "http://localhost:3000" "Web App (HTTP)"
echo ""

# Show available commands
echo "📚 Available HTTPS Commands:"
echo "  • just setup-https     - Generate certificates and configs"
echo "  • just run-https       - Run with HTTPS (foreground)"
echo "  • just run-https-d     - Run with HTTPS (background)"
echo "  • just stop-https      - Stop HTTPS services"
echo ""

# Show next steps
echo "🚀 Next Steps:"
echo "1. If not done: just setup-https"
echo "2. Update /etc/hosts file (see above)"
echo "3. Run: just run-https-d"
echo "4. Visit: https://haven.local"
echo ""
echo "📖 Full docs: docs/development/https-setup.md"