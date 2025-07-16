# Add Docker-Specific Commands to Justfile

## Description
Extend the Justfile with Docker-specific commands for containerized development workflow while maintaining existing host-based commands.

## Acceptance Criteria
- [ ] All existing commands continue to work
- [ ] New docker-* variants for containerized operations
- [ ] Commands are intuitive and well-documented
- [ ] Support both host and container workflows
- [ ] Clear naming convention for Docker commands

## New Commands to Add

### Core Development
```makefile
# Run entire stack in containers
run-docker:
    docker compose up

# Run in detached mode
run-docker-d:
    docker compose up -d

# Run only API in container (with hot-reload)
run-api-docker:
    docker compose up api

# Stop all containers
stop-docker:
    docker compose down
```

### Database Operations
```makefile
# Run migrations in container
db-migrate-docker:
    docker compose exec api alembic upgrade head

# Create migration from container
db-make-docker message:
    docker compose exec api alembic revision --autogenerate -m "{{ message }}"

# Database console via container
db-console-docker:
    docker compose exec postgres psql -U haven -d haven
```

### Testing & Quality
```makefile
# Run tests in container
test-docker:
    docker compose run --rm api pytest

# Run linting in container
lint-docker:
    docker compose run --rm api ruff check .

# Run type checking in container
type-docker:
    docker compose run --rm api pyright
```

### Utilities
```makefile
# Shell into API container
shell-docker:
    docker compose exec api /bin/bash

# Python REPL in container
shell-python-docker:
    docker compose exec api python -m asyncio

# View container logs
logs-docker service="":
    docker compose logs -f {{ service }}

# Rebuild containers
rebuild-docker:
    docker compose build --no-cache
```

### Development Helpers
```makefile
# Full reset (containers + volumes)
reset-docker:
    docker compose down -v
    docker compose up -d

# Update dependencies in container
update-docker:
    docker compose exec api pip install -e ".[dev]"
```

## Implementation Notes
- Use consistent naming: *-docker suffix
- Provide sensible defaults
- Document when to use container vs host commands
- Consider creating aliases for common workflows

## Definition of Done
- [ ] All new commands added to Justfile
- [ ] Commands tested and working
- [ ] Help text added for each command
- [ ] CLAUDE.md updated with Docker workflow
- [ ] Work log entry added