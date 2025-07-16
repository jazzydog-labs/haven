# Monitoring Guide

This guide covers monitoring, observability, and debugging Haven in production.

## Overview

Haven provides comprehensive monitoring through:

- Structured logging
- Metrics collection
- Distributed tracing
- Health checks
- Performance profiling

## Logging

### Configuration

Haven uses structured JSON logging for easy parsing:

```yaml
logging:
  level: INFO
  format: json
  structured:
    enabled: true
    include_timestamp: true
    include_level: true
    include_logger: true
```

### Log Levels

- `DEBUG` - Detailed debugging information
- `INFO` - General informational messages
- `WARNING` - Warning messages
- `ERROR` - Error messages
- `CRITICAL` - Critical issues

### Structured Log Format

```json
{
  "timestamp": "2025-01-15T12:00:00.000Z",
  "level": "INFO",
  "logger": "haven.api",
  "message": "Request processed",
  "extra": {
    "request_id": "550e8400-e29b-41d4-a716-446655440000",
    "method": "GET",
    "path": "/api/v1/records",
    "status_code": 200,
    "duration_ms": 25
  }
}
```

### Centralized Logging

Send logs to centralized systems:

#### ELK Stack

```yaml
logging:
  outputs:
    - type: elasticsearch
      hosts: ["elasticsearch:9200"]
      index: "haven-logs-%{+YYYY.MM.dd}"
```

#### CloudWatch

```python
import watchtower
logging.getLogger().addHandler(
    watchtower.CloudWatchLogHandler(
        log_group="haven",
        stream_name="production"
    )
)
```

## Metrics

### Prometheus Integration

Haven exposes metrics in Prometheus format:

```python
from prometheus_client import Counter, Histogram, Gauge

# Request metrics
request_count = Counter(
    'haven_requests_total',
    'Total requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'haven_request_duration_seconds',
    'Request duration',
    ['method', 'endpoint']
)

# Database metrics
db_connections = Gauge(
    'haven_db_connections',
    'Active database connections'
)
```

### Metrics Endpoint

```bash
# Access metrics
curl http://localhost:8080/metrics
```

### Key Metrics to Monitor

#### Application Metrics
- Request rate
- Response time (p50, p95, p99)
- Error rate
- Active connections

#### Database Metrics
- Query duration
- Connection pool usage
- Transaction rate
- Lock waits

#### System Metrics
- CPU usage
- Memory usage
- Disk I/O
- Network I/O

## Distributed Tracing

### OpenTelemetry Setup

```python
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Configure tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Configure exporter
otlp_exporter = OTLPSpanExporter(
    endpoint="http://jaeger:4317",
    insecure=True
)

# Add span processor
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)
```

### Instrumenting Code

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

@tracer.start_as_current_span("process_record")
async def process_record(record_id: str):
    span = trace.get_current_span()
    span.set_attribute("record.id", record_id)
    
    # Process record
    result = await do_processing()
    
    span.set_attribute("result.status", "success")
    return result
```

## Health Checks

### Endpoint Implementation

```python
@app.get("/health/live")
async def liveness():
    """Basic liveness check"""
    return {"status": "alive"}

@app.get("/health/ready")
async def readiness(db: AsyncSession = Depends(get_db)):
    """Readiness check including dependencies"""
    try:
        # Check database
        await db.execute("SELECT 1")
        
        # Check other dependencies
        dependencies = {
            "database": "healthy",
            "cache": check_cache_health(),
        }
        
        return {
            "status": "ready",
            "dependencies": dependencies
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "not ready", "error": str(e)}
        )
```

### Monitoring Health

Use health checks for:
- Load balancer routing
- Kubernetes probes
- Automated alerts

## Performance Monitoring

### APM Integration

#### DataDog

```python
from ddtrace import patch_all
patch_all()

# Configure
import ddtrace
ddtrace.config.service = "haven"
ddtrace.config.env = "production"
```

#### New Relic

```python
import newrelic.agent
newrelic.agent.initialize('newrelic.ini')

@newrelic.agent.function_trace()
async def critical_function():
    pass
```

### Database Query Monitoring

```python
import time
from sqlalchemy import event

@event.listens_for(Engine, "before_execute")
def before_execute(conn, clauseelement, multiparams, params):
    conn.info.setdefault("query_start_time", []).append(time.time())

@event.listens_for(Engine, "after_execute")
def after_execute(conn, clauseelement, multiparams, params, result):
    total = time.time() - conn.info["query_start_time"].pop(-1)
    logger.info(f"Query executed in {total:.3f}s", extra={
        "query": str(clauseelement),
        "duration_ms": total * 1000
    })
```

## Alerting

### Alert Rules

Define alerts based on metrics:

```yaml
# prometheus-alerts.yml
groups:
  - name: haven-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(haven_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is above 5% for 5 minutes"
      
      - alert: SlowResponse
        expr: histogram_quantile(0.95, haven_request_duration_seconds) > 1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Slow response times"
          description: "95th percentile response time is above 1s"
```

### Notification Channels

Configure alerts to send to:
- PagerDuty
- Slack
- Email
- SMS

## Debugging Production Issues

### Debug Mode

Enable debug logging temporarily:

```bash
# Set via environment
export LOG_LEVEL=DEBUG

# Or via API (if implemented)
curl -X POST http://localhost:8080/admin/debug \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{"enabled": true, "duration": 300}'
```

### Request Tracing

Trace specific requests:

```python
@app.middleware("http")
async def trace_requests(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid4()))
    
    with logger.contextualize(request_id=request_id):
        logger.info(f"Request started: {request.method} {request.url.path}")
        
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        
        logger.info(
            f"Request completed",
            extra={
                "status_code": response.status_code,
                "duration_ms": duration * 1000
            }
        )
        
        response.headers["X-Request-ID"] = request_id
        return response
```

### Memory Profiling

```python
import tracemalloc

# Start tracing
tracemalloc.start()

# Take snapshot
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

for stat in top_stats[:10]:
    print(stat)
```

## Dashboard Setup

### Grafana Dashboard

Import or create dashboards for:

1. **Overview Dashboard**
   - Request rate
   - Error rate
   - Response times
   - Active users

2. **Performance Dashboard**
   - Database query times
   - Cache hit rates
   - Memory usage
   - CPU usage

3. **Business Metrics**
   - Records created/updated
   - API usage by endpoint
   - User activity

### Example Dashboard JSON

```json
{
  "dashboard": {
    "title": "Haven Overview",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "rate(haven_requests_total[5m])"
          }
        ]
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(haven_requests_total{status=~\"5..\"}[5m])"
          }
        ]
      }
    ]
  }
}
```

## Best Practices

1. **Use Request IDs** - Track requests across services
2. **Log Strategically** - Not too much, not too little
3. **Monitor Proactively** - Set up alerts before issues occur
4. **Keep Metrics Lean** - Don't create too many labels
5. **Test Monitoring** - Verify alerts work as expected

## See Also

- [Deployment Guide](deployment.md)
- [Configuration Reference](configuration.md)
- [Troubleshooting Guide](troubleshooting.md)