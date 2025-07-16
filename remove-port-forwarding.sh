#!/bin/bash

# Remove port forwarding for Haven

echo "🧹 Removing Haven port forwarding..."
echo "===================================="
echo ""

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This script only works on macOS"
    exit 1
fi

# Disable the rules by flushing them
echo "⚡ Flushing port forwarding rules..."
sudo pfctl -F all

echo ""
echo "✅ Port forwarding disabled!"
echo ""
echo "🌐 Access URLs with port numbers:"
echo "  • http://web.haven.local:9000"
echo "  • http://haven.local:9000"
echo "  • http://api.haven.local:9000"