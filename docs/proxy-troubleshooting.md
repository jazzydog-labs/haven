# Proxy Troubleshooting Guide

## Understanding the Proxy Setup

Haven uses Caddy as a reverse proxy to route traffic to the frontend and backend services. This guide explains how the proxy works and how to troubleshoot common issues.

## Port Configuration

### Port 9000 (Default, No Sudo Required)
- **Command**: `just run-proxy`
- **Access URLs**: 
  - http://web.haven.local:9000
  - http://api.haven.local:9000
  - http://haven.local:9000
- **Advantages**: No sudo required, works immediately
- **Disadvantages**: Must include :9000 in all URLs

### Port 80 (Standard HTTP, Requires Sudo)
- **Command**: `just run-proxy80` 
- **Access URLs**:
  - http://web.haven.local (no port needed)
  - http://api.haven.local
  - http://haven.local
- **Advantages**: Clean URLs without port numbers
- **Disadvantages**: Requires sudo password when starting

## Common Issues

### "http://haven.local doesn't work"
This happens when:
1. The proxy is running on port 9000 (not 80)
2. Solution: Use http://haven.local:9000 OR run `just run-proxy80` with sudo

### "http://haven.local:3000 works but http://haven.local doesn't"
This means you're accessing the frontend directly, not through the proxy:
- Port 3000 = Direct frontend access (no proxy)
- Port 80/9000 = Through proxy (recommended)

### Multiple Frontend Instances
If you see multiple node/npm processes:
```bash
# Stop all services
just stop-all
pkill -f "npm run dev"
pkill -f caddy

# Start fresh
just run-proxy
```

## Manual Setup

If the automated commands aren't working:

```bash
# 1. Start backend
just docker::up-d

# 2. Start frontend (in a new terminal)
cd apps/web && npm run dev

# 3. Start proxy on port 9000 (in a new terminal)
caddy run --config Caddyfile.http

# OR start proxy on port 80 (requires sudo)
sudo caddy run --config Caddyfile.http80
```

## Verifying Services

Check what's running:
```bash
# Check processes
ps aux | grep -E "(caddy|npm|node|docker)"

# Check ports
lsof -i :80 -i :3000 -i :8080 -i :9000

# Test endpoints
curl http://localhost:3000          # Frontend direct
curl http://localhost:8080/health   # Backend direct
curl http://web.haven.local:9000    # Frontend via proxy
curl http://api.haven.local:9000/health  # Backend via proxy
```

## Architecture

```
User Browser
     |
     v
Caddy Proxy (port 80 or 9000)
     |
     +---> Frontend (port 3000)
     |
     +---> Backend API (port 8080)
```

The proxy allows you to:
- Access everything from one domain
- Avoid CORS issues
- Use subdomains for different services
- Route /api/* to backend, everything else to frontend