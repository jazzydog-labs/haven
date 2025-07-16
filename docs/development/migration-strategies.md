# Migration Strategies for Containerized Environment

This guide explains the different approaches for running Alembic migrations in the Haven project's containerized environment.

## Available Migration Methods

### 1. Host-based Migration (Original)
```bash
just db-migrate
```

**When to use:**
- During local development when you have Python environment set up
- When generating new migrations (requires access to models)
- When you need to quickly iterate on migration scripts

**Pros:**
- Direct access to code for debugging
- Fastest for development iteration
- No container startup overhead

**Cons:**
- Requires local Python environment setup
- Database must be accessible from host (port forwarding required)

### 2. Exec into Running Container
```bash
just db-migrate-docker
```

**When to use:**
- When API container is already running
- For quick migration runs during development
- When troubleshooting migration issues

**Pros:**
- Uses existing running container
- Has access to all application dependencies
- Good for interactive debugging

**Cons:**
- Requires API container to be running
- Not suitable for CI/CD pipelines

### 3. One-shot Container
```bash
just db-migrate-run
```

**When to use:**
- In CI/CD pipelines
- When you need to run migrations without starting the API
- For automated deployment scripts

**Pros:**
- Doesn't require running services
- Clean, isolated execution
- Perfect for automation

**Cons:**
- Slight overhead from container startup
- Creates new container each time

### 4. Dedicated Migration Service
```bash
just db-migrate-service
# or
docker compose --profile migration up migrate
```

**When to use:**
- In production deployments
- When you want explicit control over migration timing
- For complex orchestration scenarios

**Pros:**
- Clearly separated concerns
- Can be orchestrated with other services
- Minimal container with only migration dependencies

**Cons:**
- Requires profile flag to run
- Additional service to maintain

## Environment-specific Considerations

### Development
- Use method 1 (host-based) for creating new migrations
- Use method 2 (exec) for applying migrations while developing
- Hot-reload friendly - no service restarts needed

### CI/CD Pipeline
- Use method 3 (one-shot) for automated tests
- Ensures clean state for each test run
- Example GitHub Actions workflow:
```yaml
- name: Run migrations
  run: just db-migrate-run
```

### Production
- Use method 4 (dedicated service) for controlled deployments
- Can be run as a Kubernetes Job or ECS Task
- Ensures migrations complete before API starts

## Creating New Migrations

New migrations should always be created from the host or exec method:

```bash
# From host (recommended)
just db-make "add_user_table"

# From running container
just db-make-docker "add_user_table"
```

## Additional Migration Commands

All migration commands have Docker equivalents:

| Host Command | Docker Command | Description |
|--------------|----------------|-------------|
| `just db-history` | `just db-history-docker` | Show migration history |
| `just db-current` | `just db-current-docker` | Show current migration |
| `just db-downgrade` | `just db-downgrade-docker` | Rollback migrations |
| `just db-reset` | `just db-reset-docker` | Reset database completely |

## Troubleshooting

### Connection Issues
Ensure the database host is set correctly:
- From host: `localhost:5432`
- From container: `postgres:5432`

### Permission Errors
The migration service uses read-only mounts. If you need to generate migrations, use the host or exec methods.

### Timing Issues
The migration service waits for PostgreSQL health check. If migrations fail, check:
```bash
docker compose ps
docker compose logs postgres
```

## Best Practices

1. **Always test migrations locally first** using method 1 or 2
2. **Use one-shot containers in CI** for reproducible builds
3. **Use dedicated service in production** for clear deployment steps
4. **Keep migration scripts idempotent** to handle retries
5. **Monitor migration logs** in production environments