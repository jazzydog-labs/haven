# Create Docker Compose Override for Development

## Description
Create a docker-compose.override.yml file that provides development-specific configurations without modifying the base docker-compose.yml.

## Acceptance Criteria
- [ ] Override file automatically loaded by docker-compose
- [ ] Enables hot-reload for FastAPI
- [ ] Mounts source code as volumes
- [ ] Sets development environment variables
- [ ] Optionally enables debug ports
- [ ] Does not affect production deployments

## Implementation Notes

### Example docker-compose.override.yml
```yaml
version: '3.8'

services:
  api:
    build:
      target: dependencies  # Use lighter dev stage
    volumes:
      - ./apps/api/src:/app/src:delegated
      - ./apps/api/conf:/app/conf:delegated
      - ./apps/api/alembic:/app/alembic:delegated
      - ./apps/api/.venv:/app/.venv:delegated  # Optional: share venv
    environment:
      - ENVIRONMENT=local
      - DEBUG=true
      - RELOAD=true
    command: python -m uvicorn haven.main:app --reload --host 0.0.0.0 --port 8080
    stdin_open: true
    tty: true
    
  postgres:
    ports:
      - "5432:5432"  # Expose for local tools like pgAdmin
```

### Key Features
- `delegated` mount option for better macOS performance
- Interactive terminal support for debugging
- Shared virtual environment (optional)
- Development-specific environment variables

## Considerations
- Add docker-compose.override.yml to .gitignore
- Provide docker-compose.override.yml.example
- Document how to customize for individual developers
- Consider different OS performance characteristics

## Definition of Done
- [ ] Override file created and tested
- [ ] Hot-reload confirmed working
- [ ] Example file provided for team
- [ ] Documentation updated
- [ ] .gitignore updated
- [ ] Work log entry added