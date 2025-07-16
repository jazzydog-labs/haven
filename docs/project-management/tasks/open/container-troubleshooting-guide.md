# Create Container Troubleshooting Guide

## Description
Create comprehensive troubleshooting documentation for common containerization issues to reduce developer friction and support time.

## Acceptance Criteria
- [ ] Common issues documented with solutions
- [ ] Diagnostic commands provided
- [ ] Platform-specific issues addressed
- [ ] Quick reference created
- [ ] Integrated into main documentation

## Issues to Document

### Port Conflicts
- Symptoms: "Port already in use" errors
- Diagnosis: `lsof -i :8080` or `netstat -an | grep 8080`
- Solutions:
  - Stop conflicting service
  - Change port mapping in docker-compose
  - Use docker-compose port management

### Database Connection Issues
- Symptoms: "Connection refused" or "Host not found"
- Common mistakes:
  - Using localhost instead of service name
  - Wrong DATABASE_URL format
  - Service not ready yet
- Solutions provided with examples

### Volume Mount Issues
- Hot reload not working
- Permission denied errors
- File not found errors
- Performance problems on macOS

### Container Startup Issues
- Health check failures
- Dependency timing problems
- Environment variable missing
- Migration failures

### Networking Problems
- Can't access from host
- Containers can't communicate
- DNS resolution issues
- Proxy/firewall interference

## Documentation Structure
```markdown
## Troubleshooting Docker Issues

### Quick Diagnostics
- `docker ps` - Check running containers
- `docker compose logs api` - View service logs
- `docker compose exec api env` - Check environment
- `docker network ls` - List networks

### Common Issues

#### Issue: Port Already in Use
**Symptom**: Error "bind: address already in use"
**Diagnosis**: 
```bash
# macOS/Linux
lsof -i :8080
# Windows
netstat -an | findstr :8080
```
**Solutions**:
1. Stop the conflicting service
2. Change port in docker-compose.yml
3. Kill the process: `kill -9 <PID>`
```

## Definition of Done
- [ ] All common issues documented
- [ ] Solutions tested on macOS/Linux/Windows
- [ ] Quick reference card created
- [ ] Added to docs/docker.md
- [ ] Team feedback incorporated
- [ ] Work log entry added