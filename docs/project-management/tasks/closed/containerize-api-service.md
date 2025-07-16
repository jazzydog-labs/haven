# Containerize FastAPI Service with Hot-Reload

## Description
Configure FastAPI to run in a Docker container with development hot-reload support while maintaining the ability to connect to the PostgreSQL container.

## Acceptance Criteria
- [ ] FastAPI service defined in docker-compose.yml
- [ ] Hot-reload works when code changes are made
- [ ] Service can connect to PostgreSQL container
- [ ] Port 8080 is exposed and accessible from host
- [ ] Environment variables properly configured
- [ ] Health check endpoint works from container

## Implementation Notes
- Use volume mounts for source code to enable hot-reload
- Set PYTHONUNBUFFERED=1 for proper log output
- Use depends_on to ensure PostgreSQL starts first
- Consider using watchfiles or uvicorn's reload flag
- Mount both src/ and conf/ directories

## Example Configuration
```yaml
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
      target: dependencies  # Use dev stage
    volumes:
      - ./apps/api/src:/app/src
      - ./apps/api/conf:/app/conf
    ports:
      - "8080:8080"
    environment:
      DATABASE_URL: postgresql+asyncpg://haven:haven@postgres:5432/haven
    command: python -m uvicorn haven.main:app --reload --host 0.0.0.0
```

## Definition of Done
- [ ] Service starts with docker-compose up
- [ ] Code changes trigger automatic reload
- [ ] Can access API at http://api.haven.local
- [ ] GraphQL playground accessible
- [ ] Database connections work properly
- [ ] Work log entry added