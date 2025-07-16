# Deployment Guide

This guide covers deploying Haven to production environments.

## Deployment Options

### Docker Deployment

The recommended deployment method uses Docker containers.

#### Build the Image

```bash
# Build production image
docker build -t haven:latest .

# Tag for registry
docker tag haven:latest your-registry.com/haven:latest

# Push to registry
docker push your-registry.com/haven:latest
```

#### Run with Docker Compose

```yaml
version: '3.8'

services:
  haven:
    image: your-registry.com/haven:latest
    ports:
      - "8080:8080"
    environment:
      DATABASE_URL: ${DATABASE_URL}
      APP_ENV: production
      LOG_LEVEL: INFO
    depends_on:
      postgres:
        condition: service_healthy
    restart: unless-stopped

  postgres:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: haven
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

### Kubernetes Deployment

For Kubernetes deployments, use these manifests:

#### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: haven
spec:
  replicas: 3
  selector:
    matchLabels:
      app: haven
  template:
    metadata:
      labels:
        app: haven
    spec:
      containers:
      - name: haven
        image: your-registry.com/haven:latest
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: haven-secrets
              key: database-url
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

## Environment Configuration

### Required Environment Variables

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname

# Application
APP_ENV=production
APP_HOST=0.0.0.0
APP_PORT=8080

# Security
SECRET_KEY=<generate-secure-key>
CORS_ORIGINS=https://app.example.com

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

### Generate Secure Keys

```bash
# Generate secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Database Migrations

Run migrations before deploying new versions:

```bash
# Connect to production database
export DATABASE_URL=<production-database-url>

# Run migrations
alembic upgrade head
```

## Health Checks

Haven provides health endpoints for monitoring:

- `/health` - Basic health check
- `/health/ready` - Readiness check (includes DB)
- `/health/live` - Liveness check

## Monitoring

### Logging

Configure structured JSON logging for production:

```yaml
logging:
  level: INFO
  format: json
  console:
    enabled: true
    colorize: false
```

### Metrics

Haven can export metrics in Prometheus format:

```python
# Enable metrics endpoint
app.add_route("/metrics", metrics_handler)
```

### Distributed Tracing

Configure OpenTelemetry for tracing:

```bash
OTEL_EXPORTER_OTLP_ENDPOINT=http://jaeger:4317
OTEL_SERVICE_NAME=haven
OTEL_TRACES_EXPORTER=otlp
```

## Security Considerations

### HTTPS/TLS

Always use HTTPS in production:

```nginx
server {
    listen 443 ssl http2;
    server_name api.example.com;
    
    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;
    
    location / {
        proxy_pass http://haven:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### API Authentication

Enable authentication for production:

```python
# In settings
AUTH_ENABLED=true
AUTH_SECRET_KEY=<secret>
```

### Rate Limiting

Configure rate limits:

```python
# In settings
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
```

## Scaling

### Horizontal Scaling

Haven is stateless and scales horizontally:

```bash
# Docker Swarm
docker service scale haven=5

# Kubernetes
kubectl scale deployment haven --replicas=5
```

### Database Connection Pooling

Configure connection pool for scale:

```yaml
database:
  pool:
    size: 20
    max_overflow: 10
    timeout: 30
```

## Backup and Recovery

### Database Backups

Automate PostgreSQL backups:

```bash
#!/bin/bash
# backup.sh
BACKUP_DIR=/backups
DB_NAME=haven
DATE=$(date +%Y%m%d_%H%M%S)

pg_dump $DATABASE_URL > $BACKUP_DIR/haven_$DATE.sql
gzip $BACKUP_DIR/haven_$DATE.sql

# Keep last 7 days
find $BACKUP_DIR -name "haven_*.sql.gz" -mtime +7 -delete
```

### Restore Process

```bash
# Restore from backup
gunzip -c haven_20250115_120000.sql.gz | psql $DATABASE_URL
```

## Troubleshooting Production Issues

### Check Logs

```bash
# Docker
docker logs haven

# Kubernetes
kubectl logs -f deployment/haven
```

### Database Connectivity

```bash
# Test connection
python -c "
import asyncio
import asyncpg
asyncio.run(asyncpg.connect('$DATABASE_URL'))
"
```

### Performance Issues

1. Check database query performance
2. Review connection pool settings
3. Monitor memory usage
4. Check for blocking I/O

## Production Checklist

- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] HTTPS/TLS enabled
- [ ] Authentication configured
- [ ] Rate limiting enabled
- [ ] Monitoring set up
- [ ] Backup strategy implemented
- [ ] Health checks verified
- [ ] Load testing completed
- [ ] Security scan passed

## See Also

- [Docker Guide](docker.md)
- [Configuration Reference](configuration.md)
- [Monitoring Guide](monitoring.md)