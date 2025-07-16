# Configure Local CORS and Custom Domains

## Description
Set up local development environment to avoid CORS issues and simulate production-like domain configuration. Provide multiple options for different use cases.

## Acceptance Criteria
- [ ] CORS issues between frontend and backend resolved
- [ ] Custom local domains working (e.g., api.haven.local)
- [ ] Documentation for hosts file setup
- [ ] FastAPI CORS configuration properly set
- [ ] Support for both localhost and custom domain access

## Implementation Options

### Option 1: Proper CORS Configuration (Simplest)
```python
# FastAPI CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",  # Vite default
        "http://app.haven.local:3000",
        "https://app.haven.local:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Option 2: Custom Local Domains
```bash
# Add to /etc/hosts
127.0.0.1 api.haven.local
127.0.0.1 app.haven.local
127.0.0.1 haven.local

# Docker compose environment
environment:
  - ALLOWED_HOSTS=api.haven.local,localhost
  - FRONTEND_URL=http://app.haven.local:3000
```

### Option 3: Reverse Proxy (No CORS)
```yaml
# docker-compose.yml
services:
  proxy:
    image: traefik:v2.9
    ports:
      - "80:80"
    labels:
      - "traefik.http.routers.api.rule=Host(`haven.local`) && PathPrefix(`/api`)"
      - "traefik.http.routers.app.rule=Host(`haven.local`)"
```

## Configuration Requirements
- Environment-specific CORS settings
- Support multiple frontend URLs
- Document security implications
- Provide setup scripts

## Definition of Done
- [ ] CORS configuration implemented
- [ ] Local domain setup documented
- [ ] Multiple access methods work
- [ ] No CORS errors in browser console
- [ ] Setup script provided
- [ ] Work log entry added