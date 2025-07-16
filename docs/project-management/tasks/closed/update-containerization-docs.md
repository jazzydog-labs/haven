# Update Documentation for Containerized Workflow

## Description
Update CLAUDE.md and other relevant documentation to include the new containerized development workflow options.

## Acceptance Criteria
- [ ] CLAUDE.md includes containerized quickstart
- [ ] Clear explanation of when to use containers vs host
- [ ] Migration strategy documentation
- [ ] Troubleshooting section for common container issues
- [ ] Environment variable configuration explained

## Documentation Sections to Add

### Quick Start (Containerized)
```markdown
## Quick Start - Docker

```bash
# Start everything with one command
just docker::up

# Or step by step:
just database::up                  # Start PostgreSQL
just run-api-docker         # Start API with hot-reload

# Run migrations
just database::migrate-docker

# Access the services
# API: http://api.haven.local
# GraphQL: http://api.haven.local/graphql
```
```

### When to Use What
```markdown
## Development Modes

### Host-based Development
Use when:
- You need fast iteration on Python dependencies
- Debugging with local IDE
- Working on migrations/models
- Running one-off scripts

### Container-based Development  
Use when:
- Onboarding new team members
- Testing production-like environment
- Working on frontend only
- Ensuring consistent environment
```

### Migration Strategies
```markdown
## Database Migrations

### From Host (Recommended for development)
```bash
just database::make "add_user_table"    # Generate migration
just database::migrate                  # Apply migrations
```

### From Container (Recommended for CI/CD)
```bash
just database::migrate-docker           # Apply migrations
just database::make-docker "add_field"  # Generate in container
```
```

### Troubleshooting
```markdown
## Common Container Issues

### Hot-reload not working
- Ensure volumes are mounted correctly
- Check for PYTHONUNBUFFERED=1
- Verify file permissions

### Database connection errors  
- Use 'postgres' as hostname, not 'localhost'
- Check DATABASE_URL environment variable
- Ensure postgres container is healthy

### Port conflicts
- Check for existing services on 8080/5432
- Use docker ps to see running containers
```

## Definition of Done
- [ ] CLAUDE.md updated with container sections
- [ ] Choice between workflows clearly explained
- [ ] Common issues documented
- [ ] Environment setup documented
- [ ] Work log entry added