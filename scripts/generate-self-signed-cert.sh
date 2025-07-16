#!/bin/bash
# Generate self-signed certificates for local HTTPS development

set -e

echo "🔐 Generating self-signed certificates for local development"
echo "=========================================================="
echo ""

# Create certs directory
CERT_DIR="certs"
mkdir -p $CERT_DIR
cd $CERT_DIR

# Generate private key
echo "🔑 Generating private key..."
openssl genrsa -out key.pem 2048

# Generate certificate signing request
echo "📝 Creating certificate signing request..."
openssl req -new -key key.pem -out csr.pem -subj "/C=US/ST=State/L=City/O=Haven Development/CN=*.haven.local"

# Create extensions file for SANs
cat > extensions.txt << EOF
subjectAltName = DNS:haven.local, DNS:*.haven.local, DNS:api.haven.local, DNS:app.haven.local, DNS:localhost, IP:127.0.0.1
EOF

# Generate self-signed certificate
echo "📜 Generating self-signed certificate..."
openssl x509 -req -days 365 -in csr.pem -signkey key.pem -out cert.pem -extfile extensions.txt

# Clean up
rm csr.pem extensions.txt

echo "✅ Certificates generated in $CERT_DIR/"
echo ""
echo "⚠️  Note: These are self-signed certificates."
echo "   Browsers will show a security warning that you'll need to accept."
echo ""
echo "📁 Files created:"
echo "   - certs/cert.pem (certificate)"
echo "   - certs/key.pem  (private key)"

cd ..