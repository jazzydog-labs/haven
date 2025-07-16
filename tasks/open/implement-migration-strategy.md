# Implement Containerized Migration Strategy

## Description
Create multiple options for running Alembic migrations in a containerized environment, allowing flexibility for different deployment scenarios.

## Acceptance Criteria
- [ ] Migration commands work from host (existing functionality maintained)
- [ ] Migration commands work from within API container
- [ ] Optional dedicated migration service in docker-compose
- [ ] Clear documentation on when to use each approach
- [ ] Justfile commands for each migration method

## Implementation Notes

### Method 1: Host-based (Current)
```bash
just db-migrate  # Runs from local Python environment
```

### Method 2: API Container
```bash
# Add to Justfile:
db-migrate-docker:
    docker compose exec api alembic upgrade head
```

### Method 3: One-shot Container
```bash
# Add to Justfile:
db-migrate-run:
    docker compose run --rm api alembic upgrade head
```

### Method 4: Dedicated Service
```yaml
# In docker-compose.yml:
services:
  migrate:
    build: .
    command: alembic upgrade head
    environment:
      DATABASE_URL: postgresql+asyncpg://haven:haven@postgres:5432/haven
    depends_on:
      postgres:
        condition: service_healthy
    profiles: ["migration"]  # Only runs when explicitly requested
```

## Considerations
- Ensure DATABASE_URL uses container hostname (postgres) not localhost
- Handle different environments (dev/staging/prod)
- Consider CI/CD pipeline requirements
- Maintain ability to generate new migrations from host

## Definition of Done
- [ ] All migration methods tested and working
- [ ] Justfile updated with new commands
- [ ] Documentation explains pros/cons of each approach
- [ ] CI pipeline can run migrations
- [ ] Work log entry added