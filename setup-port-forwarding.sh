#!/bin/bash

# Setup port forwarding for clean URLs (macOS only)
# This allows accessing http://web.haven.local instead of http://web.haven.local:9000

set -e

echo "🔧 Setting up port forwarding for clean URLs..."
echo "================================================"
echo ""

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This script only works on macOS"
    echo "💡 Use URLs with port :9000 instead (e.g., http://web.haven.local:9000)"
    exit 1
fi

# Check if running as root
if [[ $EUID -eq 0 ]]; then
    echo "❌ Don't run this script as root"
    echo "💡 Run as normal user - it will prompt for sudo when needed"
    exit 1
fi

# Create pfctl rules file
RULES_FILE="/tmp/haven-port-forward.conf"
cat > "$RULES_FILE" << 'EOF'
# Haven port forwarding rules
# Forward HTTP port 80 to 9000 for clean URLs
rdr pass inet proto tcp from any to any port 80 -> 127.0.0.1 port 9000
pass in proto tcp from any to any port 9000
EOF

echo "📝 Created port forwarding rules..."

# Enable pfctl if not already enabled
if ! sudo pfctl -s info >/dev/null 2>&1; then
    echo "🔧 Enabling pfctl (macOS firewall)..."
    sudo pfctl -e
fi

# Load the rules
echo "⚡ Loading port forwarding rules..."
sudo pfctl -f "$RULES_FILE"

echo ""
echo "✅ Port forwarding enabled!"
echo ""
echo "🌐 You can now access:"
echo "  • http://web.haven.local (instead of :9000)"
echo "  • http://haven.local"
echo "  • http://api.haven.local"
echo ""
echo "🛑 To disable port forwarding:"
echo "  ./remove-port-forwarding.sh"
echo ""
echo "⚠️  Note: Port forwarding persists until you disable it or reboot"