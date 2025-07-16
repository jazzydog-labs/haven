# Container Troubleshooting Guide

This guide helps you diagnose and resolve common Docker and container-related issues in the Haven project.

## Quick Diagnostics

Run these commands first to understand the current state:

```bash
# Check running containers
docker compose ps

# View service logs
docker compose logs -f api
docker compose logs -f postgres

# Check container environment
docker compose exec api env | grep HAVEN

# List Docker networks
docker network ls

# Check Docker disk usage
docker system df
```

## Common Issues and Solutions

### 1. Port Already in Use

**Symptom**: 
```
Error: bind: address already in use
Error: port is already allocated
```

**Diagnosis**:
```bash
# macOS/Linux
lsof -i :8080
lsof -i :5432

# Windows
netstat -an | findstr :8080
netstat -an | findstr :5432

# Using Docker
docker port $(docker ps -q)
```

**Solutions**:
1. Stop the conflicting service:
   ```bash
   # Find and kill the process
   kill -9 $(lsof -t -i:8080)
   
   # Or stop all Docker containers
   docker compose down
   docker stop $(docker ps -aq)
   ```

2. Change port mapping in docker-compose.override.yml:
   ```yaml
   services:
     api:
       ports:
         - "8081:8080"  # Use different host port
   ```

3. Use environment variable for dynamic ports:
   ```bash
   API_PORT=8081 docker compose up
   ```

### 2. Database Connection Issues

**Symptom**:
```
sqlalchemy.exc.OperationalError: connection refused
psycopg2.OperationalError: could not connect to server
FATAL: password authentication failed
```

**Common Causes**:
- Using `localhost` instead of service name
- Database not ready yet
- Wrong credentials
- Network issues

**Solutions**:

1. Verify database is running and healthy:
   ```bash
   docker compose ps postgres
   docker compose exec postgres pg_isready
   ```

2. Check connection string:
   ```bash
   # From host machine
   DATABASE_URL=postgresql://haven:haven@localhost:5432/haven
   
   # From container (use service name)
   DATABASE_URL=postgresql://haven:haven@postgres:5432/haven
   ```

3. Test connection manually:
   ```bash
   # From host
   psql -h localhost -U haven -d haven
   
   # From container
   docker compose exec api psql -h postgres -U haven -d haven
   ```

4. Wait for database to be ready:
   ```yaml
   depends_on:
     postgres:
       condition: service_healthy
   ```

### 3. Volume Mount Issues

**Symptom**:
- Hot reload not working
- `Permission denied` errors
- `File not found` errors
- Slow performance on macOS

**Solutions**:

1. **Hot reload not working**:
   ```bash
   # Check if files are mounted
   docker compose exec api ls -la /app/src
   
   # Verify reload is enabled
   docker compose exec api env | grep RELOAD
   
   # Check logs for reload messages
   docker compose logs api | grep -i reload
   ```

2. **Permission issues**:
   ```bash
   # Fix ownership (Linux)
   sudo chown -R $(id -u):$(id -g) ./apps/api
   
   # Run container as current user
   docker compose run --user $(id -u):$(id -g) api bash
   ```

3. **macOS performance**:
   ```yaml
   # Use delegated or cached consistency
   volumes:
     - ./apps/api/src:/app/src:delegated
   ```

4. **Windows file paths**:
   ```bash
   # Use forward slashes or escaped backslashes
   # Good: C:/Users/name/project
   # Bad: C:\Users\name\project
   ```

### 4. Container Startup Failures

**Symptom**:
- Container exits immediately
- Health check failures
- Dependency errors

**Diagnosis**:
```bash
# Check exit codes
docker compose ps -a

# View startup logs
docker compose logs api | head -50

# Debug interactively
docker compose run --rm api bash
```

**Solutions**:

1. **Missing environment variables**:
   ```bash
   # List all environment variables
   docker compose config
   
   # Set required variables
   export HAVEN_DATABASE__HOST=postgres
   docker compose up
   ```

2. **Migration failures**:
   ```bash
   # Run migrations manually
   docker compose run --rm api alembic upgrade head
   
   # Check migration status
   docker compose exec api alembic current
   ```

3. **Dependency timing**:
   ```bash
   # Start services in order
   docker compose up -d postgres
   sleep 5
   docker compose up api
   ```

### 5. Networking Problems

**Symptom**:
- Can't access service from host
- Containers can't communicate
- DNS resolution fails

**Solutions**:

1. **Can't access from host**:
   ```bash
   # Check port binding
   docker compose port api 8080
   
   # Test connectivity
   curl http://localhost:8080/health
   
   # Check firewall
   sudo iptables -L -n | grep 8080
   ```

2. **Container communication**:
   ```bash
   # Test from one container to another
   docker compose exec api ping postgres
   docker compose exec api curl http://api:8080/health
   
   # Check network
   docker network inspect haven_haven-network
   ```

3. **DNS issues**:
   ```bash
   # Test DNS resolution
   docker compose exec api nslookup postgres
   
   # Use IP directly
   docker compose exec api ping 172.18.0.2
   ```

### 6. Resource Constraints

**Symptom**:
- Out of memory errors
- Disk space errors
- CPU throttling

**Solutions**:

1. **Clean up resources**:
   ```bash
   # Remove unused containers
   docker container prune -f
   
   # Remove unused images
   docker image prune -a -f
   
   # Remove unused volumes
   docker volume prune -f
   
   # Full cleanup
   docker system prune -a --volumes -f
   ```

2. **Increase Docker resources**:
   - Docker Desktop: Preferences → Resources
   - Linux: Check `docker info` for limits

3. **Monitor usage**:
   ```bash
   # Real-time stats
   docker stats
   
   # Check disk usage
   docker system df
   ```

## Platform-Specific Issues

### macOS

1. **File watching issues**:
   ```bash
   # Increase file descriptor limit
   ulimit -n 10000
   ```

2. **Performance problems**:
   - Use `:delegated` mount option
   - Consider using named volumes for dependencies
   - Enable virtualization framework in Docker Desktop

### Windows

1. **Line ending issues**:
   ```bash
   # Configure git
   git config core.autocrlf input
   ```

2. **Path issues**:
   - Use WSL2 for better compatibility
   - Mount from WSL2 filesystem, not Windows

3. **Hyper-V conflicts**:
   - Disable other virtualization software
   - Ensure Hyper-V is enabled

### Linux

1. **Permission issues**:
   ```bash
   # Add user to docker group
   sudo usermod -aG docker $USER
   newgrp docker
   ```

2. **SELinux issues**:
   ```bash
   # Add :Z flag to volumes
   volumes:
     - ./data:/data:Z
   ```

## Quick Reference Card

```bash
# Essential Commands
docker compose ps              # Show running containers
docker compose logs -f         # Stream all logs
docker compose down -v         # Stop and remove volumes
docker compose build --no-cache # Rebuild from scratch

# Debugging
docker compose exec api bash   # Shell into container
docker compose run --rm api env # Check environment
docker logs haven-api -f       # Direct container logs
docker inspect haven-api       # Full container details

# Cleanup
docker system prune -a -f      # Remove everything unused
just clean-docker              # Project-specific cleanup

# Common Fixes
just reset-docker              # Full reset
just rebuild-docker            # Force rebuild
export DOCKER_BUILDKIT=0       # Disable BuildKit if issues
```

## Still Having Issues?

1. **Check the logs thoroughly**:
   ```bash
   docker compose logs --tail=100 api | grep -i error
   ```

2. **Run in debug mode**:
   ```bash
   DEBUG=true docker compose up
   ```

3. **Isolate the problem**:
   - Try running services individually
   - Test with minimal configuration
   - Remove docker-compose.override.yml temporarily

4. **Get help**:
   - Include output of `docker compose ps`
   - Include relevant log sections
   - Mention your OS and Docker version: `docker version`

## Prevention Tips

1. **Always use `depends_on` with health checks**
2. **Set reasonable timeouts for operations**
3. **Use `.env.example` files for configuration**
4. **Document any platform-specific requirements**
5. **Keep Docker and tools updated**
6. **Monitor resource usage regularly**

Remember: Most container issues are configuration-related. Double-check environment variables, port mappings, and volume mounts before diving deeper.