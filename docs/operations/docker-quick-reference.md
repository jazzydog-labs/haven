# Docker Quick Reference Card

## Essential Commands

```bash
# Container Management
docker compose up              # Start all services
docker compose up -d           # Start in background
docker compose down            # Stop all services
docker compose down -v         # Stop and remove volumes
docker compose ps              # Show running containers
docker compose logs -f         # Stream logs (Ctrl+C to exit)

# Service-Specific
docker compose up api          # Start only API service
docker compose logs postgres   # View PostgreSQL logs
docker compose exec api bash   # Shell into API container
docker compose restart api     # Restart API service

# Haven-Specific (via Justfile)
just run-docker               # Start all services
just stop-docker              # Stop all services
just reset-docker             # Full reset (removes data)
just shell-docker             # Shell into API container
just db-console-docker        # PostgreSQL console
just test-docker              # Run tests in container
just lint-docker              # Run linting in container

# Debugging
docker compose exec api env                    # Check environment
docker compose exec api ls -la /app           # Check file mounts
docker compose port api 8080                  # Check port mapping
docker network inspect haven_haven-network    # Inspect network
docker logs haven-api --tail=50              # Last 50 log lines

# Cleanup
docker system prune -f                        # Remove unused data
docker volume prune -f                        # Remove unused volumes
docker image prune -a -f                      # Remove unused images
just clean-docker                             # Project cleanup
```

## Common Issues & Fixes

| Issue | Quick Fix |
|-------|-----------|
| Port already in use | `kill -9 $(lsof -t -i:8080)` or change port |
| Database connection refused | Use `postgres` not `localhost` in containers |
| Hot reload not working | Check volume mounts and RELOAD env var |
| Permission denied | `chmod` files or check user in Dockerfile |
| Container exits immediately | Check logs: `docker compose logs api` |
| Can't access from host | Verify port binding in docker-compose.yml |
| Out of disk space | `docker system prune -a --volumes -f` |

## Environment Variables

```bash
# Database (from container)
HAVEN_DATABASE__HOST=postgres
HAVEN_DATABASE__PORT=5432
HAVEN_DATABASE__USERNAME=haven
HAVEN_DATABASE__PASSWORD=haven
HAVEN_DATABASE__DATABASE=haven

# API Settings
ENVIRONMENT=local
DEBUG=true
RELOAD=true
LOG_LEVEL=debug
```

## File Locations

| Purpose | Host Path | Container Path |
|---------|-----------|----------------|
| Source code | `./apps/api/src` | `/app/src` |
| Config | `./apps/api/conf` | `/app/conf` |
| Migrations | `./apps/api/alembic` | `/app/alembic` |
| Logs | `./apps/api/logs` | `/app/logs` |
| Tests | `./apps/api/tests` | `/app/tests` |
| Temp files | `./.tmp` | `/app/.tmp` |
| Git repo | `./` | `/repo` (read-only) |

## URLs & Endpoints

- API: http://localhost:8080
- Health: http://localhost:8080/health
- Swagger: http://localhost:8080/docs
- GraphQL: http://localhost:8080/graphql
- PostgreSQL: localhost:5432

## Quick Diagnostics

```bash
# Is it running?
docker compose ps

# Why did it fail?
docker compose logs api | grep -i error

# Is the database ready?
docker compose exec postgres pg_isready

# Can containers talk?
docker compose exec api ping postgres

# What's the environment?
docker compose exec api env | sort
```

## Emergency Recovery

```bash
# Nuclear option - remove everything
docker compose down -v
docker system prune -a --volumes -f
rm -rf ./.tmp ./apps/api/logs

# Fresh start
just bootstrap
just db-up
just run-docker
```

---
*Keep this handy for quick troubleshooting!*