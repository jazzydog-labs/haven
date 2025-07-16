# CORS and Local Domain Configuration

This guide explains how to configure CORS and set up local domains for Haven development.

## Overview

During development, you may encounter CORS (Cross-Origin Resource Sharing) issues when the frontend and backend run on different ports. This guide provides three solutions:

1. **Proper CORS Configuration** (simplest)
2. **Custom Local Domains** (better developer experience)
3. **Reverse Proxy** (production-like, no CORS)

## Option 1: CORS Configuration (Default)

The API is pre-configured with CORS support for common development scenarios.

### Allowed Origins

The local environment allows these origins by default:
- `http://web.haven.local` - React development server
- `http://localhost:5173` - Vite development server
- `http://api.haven.local` - API documentation
- `http://app.haven.local:3000` - Custom domain for app
- `http://api.haven.local:8080` - Custom domain for API

### Customizing CORS

Edit `apps/api/conf/environment/local.yaml`:

```yaml
cors:
  allow_origins: 
    - "http://web.haven.local"
    - "http://your-custom-origin.com"
  allow_credentials: true
  allow_methods: ["*"]
  allow_headers: ["*"]
```

Or use environment variables:
```bash
export HAVEN_CORS__ALLOW_ORIGINS='["http://web.haven.local","http://localhost:5173"]'
```

## Option 2: Custom Local Domains

Using custom domains provides a better development experience and avoids some CORS issues.

### Quick Setup

```bash
# Run the setup script (requires sudo)
sudo ./scripts/setup-local-domains.sh
```

This adds the following to your `/etc/hosts`:
- `127.0.0.1 api.haven.local`
- `127.0.0.1 app.haven.local`
- `127.0.0.1 haven.local`

### Manual Setup

Add to `/etc/hosts` (macOS/Linux) or `C:\Windows\System32\drivers\etc\hosts` (Windows):

```
127.0.0.1 api.haven.local
127.0.0.1 app.haven.local
127.0.0.1 haven.local
```

### Using Custom Domains

After setup, access services at:
- API: http://api.haven.local:8080
- Frontend: http://app.haven.local:3000
- Docs: http://api.haven.local:8080/docs
- GraphQL: http://api.haven.local:8080/graphql

## Option 3: Reverse Proxy (No CORS)

The reverse proxy serves both frontend and backend from the same domain, eliminating CORS entirely.

### Start with Reverse Proxy

```bash
# Start all services with proxy
docker compose -f docker-compose.yml -f docker-compose.proxy.yml up

# Or add to your override file
cp docker-compose.proxy.yml docker-compose.override.yml
```

### Access Everything via Single Domain

With the proxy running:
- http://haven.local - Frontend
- http://haven.local/api - REST API
- http://haven.local/graphql - GraphQL
- http://haven.local/docs - API documentation

### How It Works

The Caddy reverse proxy:
1. Routes `/api/*` to the backend container
2. Routes `/graphql` to the backend container
3. Routes everything else to the frontend
4. Handles SSL termination (if configured)

## Choosing an Approach

| Approach | Pros | Cons | When to Use |
|----------|------|------|-------------|
| CORS Config | Simple, no setup | CORS errors possible | Quick development |
| Custom Domains | Better URLs, feels real | Requires hosts file edit | Team development |
| Reverse Proxy | No CORS, production-like | More complex setup | Testing deployments |

## Troubleshooting

### CORS Errors Still Appearing

1. Check browser console for the exact origin
2. Add it to `allow_origins` in config
3. Restart the API: `just run-api`
4. Clear browser cache

### Custom Domains Not Working

1. Verify hosts file entries: `cat /etc/hosts | grep haven`
2. Flush DNS cache:
   - macOS: `sudo dscacheutil -flushcache`
   - Linux: `sudo systemd-resolve --flush-caches`
   - Windows: `ipconfig /flushdns`
3. Try using IP directly: http://127.0.0.1:8080

### Proxy Connection Refused

1. Ensure API is running: `docker compose ps`
2. Check proxy logs: `docker compose logs proxy`
3. Verify Caddyfile syntax: `docker compose exec proxy caddy validate`

## Security Considerations

### Development Only

These configurations are for **development only**. In production:
- Use specific allowed origins, not wildcards
- Enable HTTPS
- Use proper domain names
- Configure security headers

### CORS Best Practices

1. Never use `allow_origins: ["*"]` in production
2. Always specify exact origins
3. Use HTTPS for all origins
4. Limit allowed methods and headers

## Next Steps

- For HTTPS setup, see [Local HTTPS Setup](local-https-setup.md)
- For production config, see [Production Environment](../operations/production-setup.md)