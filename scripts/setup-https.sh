#!/bin/bash
# Setup local HTTPS development environment with mkcert

set -e

echo "🔐 Setting up local HTTPS development environment"
echo "================================================"
echo ""

# Check if mkcert is installed
if ! command -v mkcert &> /dev/null; then
    echo "⚠️  mkcert is not installed"
    echo ""
    echo "For trusted certificates, install mkcert:"
    echo "  macOS:    brew install mkcert"
    echo "  Linux:    apt install libnss3-tools && brew install mkcert"
    echo "  Windows:  choco install mkcert"
    echo ""
    echo "Falling back to self-signed certificates..."
    echo ""
    
    # Use self-signed certificate generator
    ./scripts/generate-self-signed-cert.sh
    CERT_METHOD="self-signed"
else
    CERT_METHOD="mkcert"
fi

# Create certs directory
CERT_DIR="certs"
mkdir -p $CERT_DIR

if [ "$CERT_METHOD" = "mkcert" ]; then
    # Check if root CA is installed
    if ! mkcert -check 2>/dev/null; then
        echo "📋 Installing mkcert root CA..."
        mkcert -install
        echo "✅ Root CA installed"
    else
        echo "✅ mkcert root CA already installed"
    fi

    # Generate certificates
    echo ""
    echo "🔧 Generating certificates with mkcert..."
    cd $CERT_DIR

    # Generate cert for all our domains
    mkcert \
        "haven.local" \
        "*.haven.local" \
        "api.haven.local" \
        "app.haven.local" \
        "localhost" \
        "127.0.0.1" \
        "::1"

    # Rename for clarity
    mv haven.local+6.pem cert.pem
    mv haven.local+6-key.pem key.pem

    echo "✅ Trusted certificates generated in $CERT_DIR/"

    # Go back to root
    cd ..
fi

# Create Caddyfile for automatic HTTPS
echo ""
echo "📝 Creating Caddyfile..."
cat > Caddyfile << 'EOF'
# Caddy configuration for local HTTPS development
{
    # Local development settings
    local_certs
    auto_https disable_redirects
}

# Main domain - serves the web app
haven.local {
    reverse_proxy localhost:3000
}

# API subdomain
api.haven.local {
    reverse_proxy localhost:8080
}

# Alternative: serve everything from one domain
https://localhost {
    # API routes
    handle /api/* {
        reverse_proxy localhost:8080
    }
    
    # GraphQL
    handle /graphql* {
        reverse_proxy localhost:8080
    }
    
    # Health check
    handle /health {
        reverse_proxy localhost:8080
    }
    
    # Swagger docs
    handle /docs* {
        reverse_proxy localhost:8080
    }
    
    # Everything else goes to web app
    handle {
        reverse_proxy localhost:3000
    }
}
EOF

# Create docker-compose override for HTTPS
echo ""
echo "🐳 Creating docker-compose.https.yml..."
cat > docker-compose.https.yml << 'EOF'
# Docker Compose override for HTTPS development
# Usage: docker compose -f docker-compose.yml -f docker-compose.https.yml up

services:
  caddy:
    image: caddy:2-alpine
    container_name: haven-caddy
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
      - ./certs:/certs:ro
      - caddy_data:/data
      - caddy_config:/config
    networks:
      - haven-network
    depends_on:
      - api

  api:
    environment:
      # Update CORS to allow HTTPS origins
      CORS_ORIGINS: '["https://haven.local", "https://app.haven.local", "https://localhost"]'

volumes:
  caddy_data:
  caddy_config:
EOF

# Create nginx alternative configuration
echo ""
echo "📝 Creating nginx configuration (alternative)..."
mkdir -p nginx
cat > nginx/nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    # SSL configuration
    ssl_certificate /etc/nginx/certs/cert.pem;
    ssl_certificate_key /etc/nginx/certs/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # API server
    server {
        listen 443 ssl;
        server_name api.haven.local;

        location / {
            proxy_pass http://host.docker.internal:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }

    # Web app server
    server {
        listen 443 ssl;
        server_name app.haven.local haven.local;

        location / {
            proxy_pass http://host.docker.internal:3000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }

    # Redirect HTTP to HTTPS
    server {
        listen 80;
        server_name *.haven.local haven.local;
        return 301 https://$server_name$request_uri;
    }
}
EOF

# Update hosts file reminder
echo ""
echo "📌 Don't forget to update your hosts file!"
echo "Add these lines to /etc/hosts (or C:\\Windows\\System32\\drivers\\etc\\hosts):"
echo ""
echo "127.0.0.1    haven.local"
echo "127.0.0.1    api.haven.local"
echo "127.0.0.1    app.haven.local"
echo ""

# Create .env updates
echo "📝 Creating .env.https for frontend..."
cat > apps/web/.env.https << 'EOF'
# HTTPS API Configuration
VITE_API_URL=https://api.haven.local/api/v1
EOF

# Summary
echo ""
echo "✅ HTTPS setup complete!"
echo ""
echo "🚀 Quick Start:"
echo "  1. Update your hosts file (see above)"
echo "  2. Choose your preferred method:"
echo ""
echo "  Option A - Caddy (Recommended):"
echo "    docker compose -f docker-compose.yml -f docker-compose.https.yml up"
echo ""
echo "  Option B - Direct with certificates:"
echo "    cd apps/api && uvicorn haven.main:app --ssl-keyfile=../../certs/key.pem --ssl-certfile=../../certs/cert.pem"
echo ""
echo "  Option C - Nginx:"
echo "    docker run -p 443:443 -v $(pwd)/nginx:/etc/nginx:ro -v $(pwd)/certs:/etc/nginx/certs:ro nginx"
echo ""
echo "📱 Access your app at:"
echo "  - https://haven.local (web app)"
echo "  - https://api.haven.local (API)"
echo "  - https://api.haven.local/docs (Swagger)"
echo "  - https://api.haven.local/graphql (GraphQL)"
echo ""
echo "🔒 All certificates are trusted by your system!"