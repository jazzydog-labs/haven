# Production-Like Local Development Environment

## Description
Create a comprehensive local development setup that closely mirrors production with custom domains, HTTPS, and proper service isolation. This eliminates CORS issues and provides a realistic testing environment.

## Acceptance Criteria
- [ ] Single domain serves both API and frontend (like production)
- [ ] HTTPS enabled with trusted certificates
- [ ] No CORS configuration needed
- [ ] Path-based routing (/api/* → API, /* → Frontend)
- [ ] WebSocket support for hot reload
- [ ] Simple startup process

## Architecture

```
https://haven.local
├── /          → Frontend (React)
├── /api       → REST API
├── /graphql   → GraphQL endpoint
├── /docs      → API documentation
└── /ws        → WebSocket (hot reload)
```

## Implementation with Traefik

```yaml
# docker-compose.yml
version: '3.8'

services:
  traefik:
    image: traefik:v2.9
    command:
      - --api.insecure=true
      - --providers.docker=true
      - --entrypoints.web.address=:80
      - --entrypoints.websecure.address=:443
    ports:
      - "80:80"
      - "443:443"
      - "8090:8080"  # Traefik dashboard
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./certs:/certs:ro
      - ./traefik.yml:/etc/traefik/traefik.yml:ro

  api:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.api.rule=Host(`haven.local`) && PathPrefix(`/api`, `/graphql`, `/docs`)"
      - "traefik.http.routers.api.entrypoints=websecure"
      - "traefik.http.routers.api.tls=true"
      - "traefik.http.services.api.loadbalancer.server.port=8080"

  web:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.web.rule=Host(`haven.local`)"
      - "traefik.http.routers.web.entrypoints=websecure"
      - "traefik.http.routers.web.tls=true"
      - "traefik.http.services.web.loadbalancer.server.port=3000"
```

## Setup Script
```bash
#!/bin/bash
# setup-local-env.sh

echo "Setting up production-like local environment..."

# 1. Add hosts entry
echo "127.0.0.1 haven.local" | sudo tee -a /etc/hosts

# 2. Generate certificates
mkcert haven.local

# 3. Move certificates
mkdir -p certs
mv haven.local*.pem certs/

# 4. Start services
docker compose up -d

echo "✅ Setup complete! Access https://haven.local"
```

## Benefits
1. **No CORS** - Same origin for everything
2. **Production-like** - Mimics real deployment
3. **HTTPS everywhere** - Test secure features
4. **Simple URLs** - Just haven.local
5. **Hot reload works** - WebSocket proxy included

## Environment Variables
```env
# .env.local
PUBLIC_URL=https://haven.local
API_URL=https://haven.local/api
DOMAIN=haven.local
HTTPS=true
```

## Alternative: Caddy (Simpler)
```
# Caddyfile
haven.local {
    handle /api/* {
        reverse_proxy api:8080
    }
    
    handle /graphql {
        reverse_proxy api:8080
    }
    
    handle {
        reverse_proxy web:3000
    }
}
```

## Definition of Done
- [ ] Traefik/Caddy configuration complete
- [ ] HTTPS working with mkcert
- [ ] Single domain serves all services
- [ ] Setup script created and tested
- [ ] Documentation includes troubleshooting
- [ ] Team onboarding tested
- [ ] Work log entry added