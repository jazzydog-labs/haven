#!/bin/bash
# Setup /etc/hosts entries for Haven local development

set -e

echo "🌐 Setting up local domain mappings"
echo "==================================="
echo ""

# Handle remove flag
if [ "$1" = "--remove" ]; then
    # Check if running as root/sudo
    if [ "$EUID" -ne 0 ]; then 
        echo "❌ This script needs sudo privileges to modify /etc/hosts"
        echo "Please run: sudo $0 --remove"
        exit 1
    fi
    
    echo "🧹 Removing Haven domain mappings"
    if grep -q "# Haven local development" /etc/hosts 2>/dev/null; then
        sed -i.haven.bak '/# Haven local development/,/# End Haven local development/d' /etc/hosts
        echo "✅ Removed hosts entries"
        echo "📋 Backup saved to /etc/hosts.haven.bak"
    else
        echo "⏭️  No Haven entries found in /etc/hosts"
    fi
    exit 0
fi

# Check if running as root/sudo for add operation
if [ "$EUID" -ne 0 ]; then 
    echo "❌ This script needs sudo privileges to modify /etc/hosts"
    echo "Please run: sudo $0"
    exit 1
fi

# Define our hosts entries
HOSTS_ENTRIES=(
    "# Haven local development"
    "127.0.0.1    haven.local"
    "127.0.0.1    web.haven.local"
    "127.0.0.1    api.haven.local"
    "127.0.0.1    app.haven.local"
    "# End Haven local development"
)

# Backup hosts file
if [ ! -f /etc/hosts.haven.backup ]; then
    cp /etc/hosts /etc/hosts.haven.backup
    echo "✅ Created backup at /etc/hosts.haven.backup"
fi

# Check if our block already exists
if grep -q "# Haven local development" /etc/hosts; then
    echo "⏭️  Haven entries already exist in /etc/hosts"
    echo ""
    echo "📋 Current Haven entries in /etc/hosts:"
    grep "haven.local" /etc/hosts | sed 's/^/   /'
    exit 0
fi

echo ""
echo "📝 Adding Haven host entries as a block..."
echo ""

# Add all entries as a block
for entry in "${HOSTS_ENTRIES[@]}"; do
    echo "$entry" >> /etc/hosts
done

echo "✅ Added Haven local development entries"

echo ""
echo "📋 Current Haven entries in /etc/hosts:"
grep "haven.local" /etc/hosts | sed 's/^/   /'

echo ""
echo "✅ Host configuration complete!"
echo ""
echo "🌐 You can now access:"
echo "   http://haven.local       - Main domain"
echo "   http://web.haven.local   - Frontend"
echo "   http://api.haven.local   - Backend API"
echo "   http://app.haven.local   - Alternative frontend"
echo ""
echo "📌 To remove these entries later:"
echo "   just remove-hosts"