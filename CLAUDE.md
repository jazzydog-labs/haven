# CLAUDE.md - Fast Development Operations

## Quick Start

```bash
# Bootstrap everything in one go
just bootstrap && just db-up && just run

# Service is now running at http://localhost:8080
# GraphiQL: http://localhost:8080/graphql
# Swagger: http://localhost:8080/docs
```

## Fast Development Workflow

### Daily Commands
```bash
just run          # Start service with hot-reload
just db-up        # Start PostgreSQL
just test-fast    # Run unit tests only (quick feedback)
just lint         # Quick syntax check
just check        # Full quality gates (lint + type + test)
```

### Development Cycle
1. Pick a task from roadmap/todo
2. Implement the feature
3. Run `just check` to verify quality
4. **Commit immediately** - don't batch changes
5. Move to next task

Each task should result in at least one atomic commit!

### Batch Operations
```bash
# Add complete CRUD for new entity
just add-entity User

# Generate and apply migration
just db-make "add_users_table" && just db-migrate

# Run specific test file
just test tests/test_api.py::test_create_record
```

## Project Context

### Architecture
- **API Layer**: FastAPI (REST) + Strawberry (GraphQL) at :8080
- **Database**: PostgreSQL via SQLAlchemy 2.x async
- **Config**: Hydra for multi-env support
- **Testing**: pytest with 70% coverage target

For detailed architecture patterns and layer responsibilities, see `docs/architecture.md`.

### Key Directories
```
src/
  domain/       # Business logic, entities
  application/  # Use cases, services  
  infrastructure/  # DB, external services
  interface/    # API routes, GraphQL schema
tests/          # Mirrors src/ structure
conf/           # Hydra configs by environment
alembic/        # Database migrations
```

## Common Tasks

### Add New REST Endpoint
```python
# 1. Add to src/interface/api/routes.py
@router.post("/items")
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    return await create_item_in_db(db, item)

# 2. Test immediately
just test-fast tests/interface/api/test_routes.py
```

### Add GraphQL Query
```python
# 1. Add to src/interface/graphql/schema.py
@strawberry.type
class Query:
    @strawberry.field
    async def items(self, info: Info) -> list[Item]:
        db = info.context["db"]
        return await get_all_items(db)

# 2. Check GraphiQL at http://localhost:8080/graphql
```

### Create Migration
```bash
# Make changes to models in src/domain/models.py
just db-make "add_status_to_items"
just db-migrate
```

### Quick Debugging
```bash
# Check logs
just logs

# Database console
just db-console

# Python REPL with app context
just shell
```

## Quality Gates (Run Before Commit)

```bash
# Quick validation
just lint          # Ruff check (5 seconds)

# Full validation  
just check         # Lint + Type + Test (30 seconds)

# Fix formatting
just format        # Auto-fix style issues
```

See `docs/quality.md` for linting/typing details and `docs/definition-of-done.md` for complete checklist.

## Implementation Status

### Current Phase: Initial Setup (Commit 0)
- [x] Project structure
- [x] Documentation framework
- [ ] Core dependencies
- [ ] Database setup
- [ ] Basic API scaffold

### Next Tasks
1. Install core dependencies (FastAPI, SQLAlchemy, etc.)
2. Set up database models and Alembic
3. Create basic REST/GraphQL endpoints
4. Add health check endpoint

### Progress Tracking
- `docs/commits-plan.md` - Detailed implementation phases
- `docs/roadmap.md` - Features, tech debt, and long-term planning
- `todo.md` - Immediate tasks and notes

Currently on commit 0 of 11 planned commits.

## Tips for Speed

1. **Skip Pre-commit Initially**: Focus on features, run quality checks in batches
2. **Use Hot Reload**: Changes apply instantly, no restart needed
3. **Test Specific Files**: `just test path/to/test.py` instead of full suite
4. **GraphiQL for Quick Tests**: Faster than writing integration tests
5. **Docker Compose**: Everything runs in containers, no local setup

## Emergency Commands

```bash
# Reset everything
just clean && just db-reset

# Stop all services
just down

# View all available commands
just --list
```

---

*This file is designed for rapid development. Quality gates and full testing come after feature implementation.*

## Documentation Directory

### Core Documentation
- **`docs/spec.md`** - Project requirements and success criteria
- **`docs/overview.md`** - Complete documentation map
- **`docs/architecture.md`** - Clean Architecture patterns and layer design
- **`docs/roadmap.md`** - Development timeline and technical debt tracking

### Developer Guides  
- **`docs/local-setup.md`** - Environment setup and prerequisites
- **`docs/testing.md`** - Test strategy, fixtures, and coverage requirements
- **`docs/quality.md`** - Linting, type checking, and code standards
- **`docs/definition-of-done.md`** - Complete checklist for task completion
- **`docs/configuration.md`** - Hydra configuration management
- **`docs/alembic.md`** - Database migration workflows
- **`docs/refactoring.md`** - Safe code reorganization procedures

### API References
- **`docs/api/rest.md`** - REST endpoints with examples
- **`docs/api/graphql.md`** - GraphQL schema and queries

### Operations
- **`docs/docker.md`** - Container build and security practices

### When to Read Which Doc

1. **Starting fresh?** → `docs/local-setup.md` then `docs/spec.md`
2. **Adding a feature?** → `docs/architecture.md` then relevant API docs
3. **Database changes?** → `docs/alembic.md`
4. **Cleaning up code?** → `docs/refactoring.md`
5. **Before committing?** → `docs/definition-of-done.md`
6. **Lost or confused?** → `docs/overview.md` for the complete map

**Remember**: Complete task → Run checks → Commit → Next task. Never leave work uncommitted!