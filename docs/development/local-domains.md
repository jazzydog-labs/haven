# Local Domain Configuration

## Overview

Haven supports local domain mappings to provide a more production-like development experience. Instead of accessing services via `localhost:port`, you can use friendly domain names like `web.haven.local` and `api.haven.local`.

## Quick Start

```bash
# Setup local domains
just setup-hosts

# Run with reverse proxy (recommended)
just run-proxy

# Access services
# Frontend: http://haven.local
# API: http://api.haven.local
# GraphQL: http://api.haven.local/graphql
```

## Domain Mappings

The following domains are configured:

| Domain | Maps To | Purpose |
|--------|---------|---------|
| `haven.local` | localhost:3000 | Main application entry |
| `web.haven.local` | localhost:3000 | Frontend application |
| `api.haven.local` | localhost:8080 | Backend API |
| `app.haven.local` | localhost:3000 | Alternative frontend alias |

## Setup Methods

### Method 1: Direct Port Access (with hosts file)

```bash
# Setup hosts entries
just setup-hosts

# Run normally
just run

# Access with domains + ports
# http://web.haven.local:3000
# http://api.haven.local:8080
```

### Method 2: Reverse Proxy (recommended)

```bash
# Setup and run with proxy
just run-proxy

# Access with clean URLs (no ports)
# http://haven.local
# http://web.haven.local
# http://api.haven.local
```

## Managing Hosts Entries

### Add Entries
```bash
just setup-hosts
```

This command:
- Adds Haven domain mappings to `/etc/hosts`
- Creates a backup at `/etc/hosts.haven.backup`
- Requires sudo permissions
- Is idempotent (safe to run multiple times)

### Remove Entries
```bash
just remove-hosts
```

This command:
- Removes all Haven entries from `/etc/hosts`
- Creates a backup before removal
- Requires sudo permissions

## Reverse Proxy Configuration

The reverse proxy uses Caddy to:
- Serve all domains on standard HTTP port 80
- Route requests to appropriate backend services
- Support HTTPS with local certificates (if configured)
- Eliminate CORS issues between frontend and backend

### Proxy Routes

```
haven.local → localhost:3000 (frontend)
web.haven.local → localhost:3000 (frontend)
api.haven.local → localhost:8080 (backend)
app.haven.local → localhost:3000 (frontend)
```

## Benefits

1. **Production-like URLs**: Use domain names instead of localhost:port
2. **No CORS Issues**: Single domain origin when using proxy
3. **Easy Service Discovery**: Memorable URLs for each service
4. **HTTPS Support**: Can use with local certificates
5. **Better Testing**: More realistic environment

## Troubleshooting

### Permission Denied
```bash
# If you see permission errors, ensure you're using sudo
sudo just setup-hosts
```

### Domains Not Resolving
```bash
# Check hosts file entries
grep haven.local /etc/hosts

# Flush DNS cache (macOS)
sudo dscacheutil -flushcache

# Flush DNS cache (Linux)
sudo systemctl restart systemd-resolved
```

### Port Conflicts
```bash
# Check if ports are in use
lsof -i :80
lsof -i :3000
lsof -i :8080

# Stop conflicting services or use different ports
```

### Proxy Not Starting
```bash
# Check if Caddy is installed
which caddy

# Install Caddy if needed
brew install caddy  # macOS
```

## Windows Users

Windows users need to manually edit the hosts file:

1. Open Notepad as Administrator
2. Open `C:\Windows\System32\drivers\etc\hosts`
3. Add these lines:
   ```
   127.0.0.1    haven.local
   127.0.0.1    web.haven.local
   127.0.0.1    api.haven.local
   127.0.0.1    app.haven.local
   ```
4. Save the file

## Related Documentation

- [HTTPS Setup](./https-setup.md) - Configure HTTPS with local domains
- [CORS and Domains](./cors-and-domains.md) - CORS configuration details
- [Docker Development](../operations/docker.md) - Container-based development