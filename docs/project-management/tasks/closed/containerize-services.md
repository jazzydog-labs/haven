# Containerize PostgreSQL and FastAPI Services

## Description
Set up PostgreSQL and FastAPI to run in separate Docker containers with proper networking and port exposure. Ensure development workflow remains smooth with hot-reload, migrations, and model changes.

## Acceptance Criteria
- [ ] PostgreSQL runs in its own container with exposed port (5432)
- [ ] FastAPI runs in its own container with exposed port (8080)
- [ ] Containers can communicate via Docker network
- [ ] Alembic migrations can be run from either container or host
- [ ] Hot-reload works for FastAPI during development
- [ ] Database data persists between container restarts
- [ ] Simple commands to start/stop all services

## Implementation Notes
- Use Docker Compose for orchestration
- Create shared network for inter-container communication
- Mount source code as volume for hot-reload
- Consider separate Dockerfile for migrations
- Ensure database URL uses container hostname

## Definition of Done
- [ ] Docker Compose configuration complete
- [ ] Both services start with `docker-compose up`
- [ ] Can run migrations with simple command
- [ ] Documentation updated in CLAUDE.md
- [ ] Tests pass in containerized environment
- [ ] Work log entry added