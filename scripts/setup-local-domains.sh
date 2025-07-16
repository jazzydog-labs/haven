#!/bin/bash

# Script to set up local domains for Haven development
# This avoids CORS issues and simulates production-like domain configuration

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then 
    echo -e "${YELLOW}This script needs to modify /etc/hosts.${NC}"
    echo "Please run with sudo: sudo $0"
    exit 1
fi

# Domains to add
DOMAINS=(
    "api.haven.local"
    "app.haven.local"
    "haven.local"
)

# Backup hosts file
HOSTS_FILE="/etc/hosts"
BACKUP_FILE="/etc/hosts.backup.$(date +%Y%m%d_%H%M%S)"

echo -e "${GREEN}Setting up local domains for Haven...${NC}"
echo "Backing up hosts file to: $BACKUP_FILE"
cp "$HOSTS_FILE" "$BACKUP_FILE"

# Function to add domain if not exists
add_domain() {
    local domain=$1
    if grep -q "$domain" "$HOSTS_FILE"; then
        echo -e "${YELLOW}Domain $domain already exists in hosts file${NC}"
    else
        echo "127.0.0.1 $domain" >> "$HOSTS_FILE"
        echo -e "${GREEN}Added $domain to hosts file${NC}"
    fi
}

# Add domains
echo -e "\n${GREEN}Adding domains to hosts file...${NC}"
for domain in "${DOMAINS[@]}"; do
    add_domain "$domain"
done

# Verify additions
echo -e "\n${GREEN}Current Haven domains in hosts file:${NC}"
grep "haven.local" "$HOSTS_FILE" || echo "No Haven domains found"

# Instructions
echo -e "\n${GREEN}Setup complete!${NC}"
echo -e "\nYou can now access Haven services at:"
echo -e "  - API: ${GREEN}http://api.haven.local:8080${NC}"
echo -e "  - App: ${GREEN}http://app.haven.local:3000${NC} (or :5173 for Vite)"
echo -e "  - Combined: ${GREEN}http://haven.local${NC} (requires reverse proxy)"
echo -e "\nTo remove these entries later, edit $HOSTS_FILE"
echo -e "Backup saved at: $BACKUP_FILE"

# Platform-specific cache clearing
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo -e "\n${YELLOW}Flushing DNS cache on macOS...${NC}"
    sudo dscacheutil -flushcache
    sudo killall -HUP mDNSResponder 2>/dev/null || true
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Check for systemd-resolved
    if systemctl is-active --quiet systemd-resolved; then
        echo -e "\n${YELLOW}Flushing DNS cache on Linux...${NC}"
        sudo systemd-resolve --flush-caches
    fi
fi

echo -e "\n${GREEN}Done!${NC}"