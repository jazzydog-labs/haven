# Local HTTPS Development Setup

## Description
Enable HTTPS for local development to support secure cookies, OAuth flows, and production-like testing. Provide multiple approaches for different needs.

## Acceptance Criteria
- [ ] HTTPS working locally with trusted certificates
- [ ] Both API and frontend accessible via HTTPS
- [ ] No browser security warnings
- [ ] OAuth redirect flows work
- [ ] Secure cookies function properly
- [ ] Easy setup process for team members

## Implementation Options

### Option 1: mkcert (Recommended)
```bash
# Install mkcert
brew install mkcert  # macOS
mkcert -install      # Install root CA

# Generate certificates
mkcert haven.local api.haven.local app.haven.local localhost

# Use in Docker/FastAPI
# Mount certificates and configure
```

### Option 2: Caddy Server (Automatic HTTPS)
```yaml
# docker-compose.yml
services:
  caddy:
    image: caddy:2-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
      - caddy_config:/config

# Caddyfile
haven.local {
  reverse_proxy api:8080
}

app.haven.local {
  reverse_proxy web:3000
}
```

### Option 3: nginx with Self-Signed Certs
```nginx
server {
    listen 443 ssl;
    server_name api.haven.local;
    
    ssl_certificate /etc/nginx/certs/cert.pem;
    ssl_certificate_key /etc/nginx/certs/key.pem;
    
    location / {
        proxy_pass http://api:8080;
    }
}
```

### Option 4: Development HTTPS Proxy
```yaml
# Using local-ssl-proxy
services:
  ssl-proxy:
    image: cameronhunter/local-ssl-proxy
    ports:
      - "443:443"
    environment:
      - TARGET=http://api:8080
      - CERT_PATH=/certs
```

## Certificate Management
- Store dev certificates in `certs/` (gitignored)
- Provide certificate generation script
- Document certificate trust process
- Consider certificate expiration

## Browser Configuration
```javascript
// Frontend configuration
const API_URL = process.env.NODE_ENV === 'development' 
  ? 'https://api.haven.local'
  : 'https://api.production.com';

// Handle self-signed certs in dev
if (process.env.NODE_ENV === 'development') {
  process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
}
```

## Security Considerations
- Never commit certificates
- Document that these are DEV ONLY
- Explain security implications
- Provide production transition guide

## Definition of Done
- [ ] HTTPS working for all services
- [ ] Certificates properly trusted
- [ ] Setup script created
- [ ] Team documentation complete
- [ ] OAuth flows tested
- [ ] Secure cookies verified
- [ ] Work log entry added