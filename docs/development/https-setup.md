# Local HTTPS Development Setup

This guide explains how to set up HTTPS for local development to support secure cookies, OAuth flows, and production-like testing.

## Quick Start

```bash
# Setup HTTPS (generates certificates and configs)
just setup-https

# Update your hosts file
sudo nano /etc/hosts
# Add:
# 127.0.0.1    haven.local
# 127.0.0.1    api.haven.local
# 127.0.0.1    app.haven.local

# Run with HTTPS
just run-https-d

# Access services
# https://haven.local (web app)
# https://api.haven.local (API)
```

## Certificate Options

### Option 1: mkcert (Recommended for Trusted Certs)

If you have mkcert installed, the setup script will generate trusted certificates:

```bash
# Install mkcert first
brew install mkcert  # macOS
mkcert -install      # Install root CA

# Then run setup
just setup-https
```

Benefits:
- ✅ No browser warnings
- ✅ Trusted by system
- ✅ Works with all browsers

### Option 2: Self-Signed Certificates (Default)

If mkcert is not available, the setup will generate self-signed certificates:

```bash
just setup-https
```

Note: You'll need to accept the security warning in your browser.

## Running with HTTPS

### Using Caddy (Recommended)

Caddy provides automatic HTTPS with proper reverse proxy:

```bash
# Run in foreground
just run-https

# Run in background
just run-https-d

# Stop services
just stop-https
```

### Direct with Uvicorn

For development without Docker:

```bash
cd apps/api
uvicorn haven.main:app \
  --ssl-keyfile=../../certs/key.pem \
  --ssl-certfile=../../certs/cert.pem \
  --host 0.0.0.0 \
  --port 8443
```

### Using Nginx

Alternative reverse proxy option:

```bash
docker run -p 443:443 \
  -v $(pwd)/nginx:/etc/nginx:ro \
  -v $(pwd)/certs:/etc/nginx/certs:ro \
  nginx
```

## Frontend Configuration

The setup creates `.env.https` for the frontend:

```bash
# Use HTTPS environment
cd apps/web
cp .env.https .env
npm run dev
```

Or set the environment variable directly:

```bash
VITE_API_URL=https://api.haven.local/api/v1 npm run dev
```

## Browser Setup

### Chrome/Edge
1. Navigate to https://haven.local
2. If using self-signed cert, click "Advanced" → "Proceed to haven.local"
3. For trusted experience, use mkcert

### Firefox
1. Navigate to https://haven.local
2. Click "Advanced" → "Accept the Risk and Continue"
3. May need to accept for each subdomain

### Safari
1. Navigate to https://haven.local
2. Click "Show Details" → "visit this website"
3. Enter system password to trust certificate

## Testing HTTPS Features

### Secure Cookies

```javascript
// API sets secure cookies
response.set_cookie(
    key="session",
    value=token,
    secure=True,      // Only sent over HTTPS
    httponly=True,    // Not accessible via JS
    samesite="strict" // CSRF protection
)
```

### OAuth Redirects

HTTPS enables proper OAuth flows:

```javascript
// OAuth providers require HTTPS callbacks
const redirectUri = 'https://haven.local/auth/callback';
```

### Service Workers

HTTPS is required for service workers:

```javascript
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js');
}
```

## Troubleshooting

### Certificate Errors

**Problem**: Browser shows "NET::ERR_CERT_AUTHORITY_INVALID"

**Solution**: 
- Use mkcert for trusted certificates
- Or manually trust the self-signed certificate
- Check certificate is valid: `openssl x509 -in certs/cert.pem -text`

### Port Conflicts

**Problem**: "bind: address already in use"

**Solution**:
```bash
# Find process using port 443
sudo lsof -i :443

# Kill process or use different port
just stop-https
```

### Hosts File Not Working

**Problem**: haven.local not resolving

**Solution**:
```bash
# Flush DNS cache
# macOS
sudo dscacheutil -flushcache

# Linux
sudo systemctl restart systemd-resolved

# Windows (as admin)
ipconfig /flushdns
```

### Mixed Content Warnings

**Problem**: "Mixed Content: The page was loaded over HTTPS, but requested an insecure resource"

**Solution**:
- Ensure all resources use HTTPS
- Update API URLs to use https://
- Check for hardcoded http:// URLs

## Production Considerations

⚠️ **Important**: These certificates are for development only!

For production:
1. Use real certificates from Let's Encrypt or other CA
2. Configure proper SSL/TLS settings
3. Enable HSTS headers
4. Use strong cipher suites
5. Regular certificate renewal

## Advanced Configuration

### Custom Domains

Edit the setup script to add more domains:

```bash
mkcert \
  "myapp.local" \
  "*.myapp.local" \
  "api.myapp.local"
```

### Multiple Projects

Share certificates across projects:

```bash
# Create shared certificate directory
mkdir ~/dev-certs
cd ~/dev-certs
mkcert "*.local"

# Link in projects
ln -s ~/dev-certs/certs ./certs
```

### Certificate Details

View certificate information:

```bash
# View certificate details
openssl x509 -in certs/cert.pem -text -noout

# Verify certificate chain
openssl verify -CAfile certs/cert.pem certs/cert.pem

# Test HTTPS connection
openssl s_client -connect haven.local:443
```

## Clean Up

To remove HTTPS setup:

```bash
# Remove certificates
rm -rf certs/

# Remove generated files
rm -f Caddyfile docker-compose.https.yml
rm -rf nginx/
rm -f apps/web/.env.https

# Remove hosts entries
sudo nano /etc/hosts
# Remove haven.local entries
```