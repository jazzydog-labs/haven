# CLAUDE.md - Fast Development Operations

## Quick Start

### 🚀 ONE COMMAND TO RUN EVERYTHING
```bash
# Start EVERYTHING (backend + frontend with hot-reload)
just run

# Or with local domains on port 9000:
just run-proxy

# Or with local domains on port 80 (requires sudo password):
# Note: You'll be prompted for your password when running this command
just run-proxy80

# Access your app:
# With run-proxy (port 9000):
# 🌐 Frontend:    http://web.haven.local:9000
# 📚 API Docs:    http://api.haven.local:9000/docs
# 🔮 GraphQL:     http://api.haven.local:9000/graphql

# With run-proxy80 (port 80, no port needed in URL):
# 🌐 Frontend:    http://web.haven.local
# 📚 API Docs:    http://api.haven.local/docs
# 🔮 GraphQL:     http://api.haven.local/graphql

# Stop everything:
just stop-all      # (or stop-proxy if using domains)

# Manual proxy setup (if automated commands don't work):
# 1. Start backend: just docker::up-d
# 2. Start frontend: cd apps/web && npm run dev
# 3. Start proxy on port 9000: caddy run --config Caddyfile.http
# 4. Or on port 80 (with sudo): sudo caddy run --config Caddyfile.http80
```

### Alternative Methods
```bash
# Backend only
just docker::up-d

# Frontend only  
cd apps/web && npm run dev

# HTTPS mode
just setup-https && just run-https
```

## Fast Development Workflow

### Daily Commands
```bash
just run              # Start service with hot-reload
just database::up     # Start PostgreSQL
just testing::fast    # Run unit tests only (quick feedback)
just lint             # Quick syntax check
just check            # Full quality gates (lint + type + test)
```

### Development Cycle
1. Pick a task from roadmap/todo or `docs/project-management/tasks/open/`
2. Implement the feature
3. Run `just check` to verify quality
4. **Commit immediately** - don't batch changes
5. **Update tracking files** - Keep everything in sync:
   - Append entry to `docs/project-management/work-log.md`
   - Update `docs/project-management/todo.md` to mark task complete
   - Update `docs/project-management/roadmap.md` if milestone achieved
   - Update `docs/project-management/commits-plan.md` if following plan
   - Update `CLAUDE.md` if new workflow added
6. Move task to `docs/project-management/tasks/closed/` if complete
7. Move to next task

Each task should result in at least one atomic commit and synchronized documentation!

### Batch Operations
```bash
# Add complete CRUD for new entity
just api::add-entity User

# Generate and apply migration
just database::make "add_users_table" && just database::migrate

# Run specific test file
just test tests/test_api.py::test_create_record
```

## Project Context

### Architecture
- **API Layer**: FastAPI (REST) + Strawberry (GraphQL) at api.haven.local
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

### Create New Task
```bash
# Create task file with descriptive name
touch tasks/open/feature-name.md

# Follow template: Title, Description, Acceptance Criteria, Implementation Notes, Definition of Done
# See docs/tasks-workflow.md for complete workflow
```

### Add New Workflow
```bash
# Create workflow documentation in docs/
touch docs/workflow-name.md

# Include: Overview, When to Use, Steps, Examples, Tools/Commands
# Add to CLAUDE.md Developer Guides section
# Reference from relevant Common Tasks sections
# Workflows are reusable processes, not one-time tasks
```

### Add New REST Endpoint
```python
# 1. Add to src/interface/api/routes.py
@router.post("/items")
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    return await create_item_in_db(db, item)

# 2. Test immediately
just testing::fast tests/interface/api/test_routes.py
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

# 2. Check GraphiQL at http://api.haven.local/graphql
```

### Create Migration
```bash
# Make changes to models in src/domain/models.py
just database::make "add_status_to_items"
just database::migrate
```

### Quick Debugging
```bash
# Check logs
just logs

# Database console
just database::console

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

### ✅ Completed Phases
- [x] **Original 11-commit plan** - All core infrastructure complete
- [x] **Monorepo transformation** - Python API + React client structure
- [x] **Git diff generation API** - Background processing with HTML export
- [x] **Containerization Phase 1** - Docker setup with hot-reload and dev tools

### Current Focus: Containerization Phase 2
**Next tasks to implement:**
1. Create docker-compose.override.yml for dev-specific settings
2. Implement multiple migration strategies for containers
3. Create container troubleshooting guide

### Progress Tracking
- `docs/project-management/commits-plan.md` - ✅ Original plan complete (commits 0-11)
- `docs/project-management/roadmap.md` - Current sprint and feature backlog
- `docs/project-management/todo.md` - Immediate tasks and priorities
- `docs/project-management/work-log.md` - Completed work with demo commands
- `docs/project-management/tasks/open/` - Active tasks ready for implementation
- `docs/project-management/tasks/closed/` - Completed tasks archive

**Project Status**: Production-ready with containerization enhancements in progress.

## Docker Workflow

### Common Docker Commands
```bash
# Development
just docker::up-d      # Start all services in background
just docker::down      # Stop all services
just docker::logs api  # View API logs
just docker::shell     # Shell into API container

# Database
just database::migrate-docker             # Run migrations in Docker
just database::make-docker "add_users"   # Create migration in Docker
just database::console-docker             # Database console via Docker

# Testing & Quality
just docker::test      # Run tests in container
just docker::lint      # Run linting in container
just docker::type-check # Type checking in container

# Utilities
just docker::ps        # Show running containers
just docker::rebuild   # Rebuild containers
just docker::reset     # Full reset (data loss!)
```

### Docker vs Local Commands
- All Docker commands end with `-docker` suffix
- Docker commands work without local Python/Node setup
- Use Docker for consistent environment across team
- Use local for faster iteration during development

## Tips for Speed

1. **Skip Pre-commit Initially**: Focus on features, run quality checks in batches
2. **Use Hot Reload**: Changes apply instantly, no restart needed
3. **Test Specific Files**: `just test path/to/test.py` instead of full suite
4. **GraphiQL for Quick Tests**: Faster than writing integration tests
5. **Docker Compose**: Everything runs in containers, no local setup

## Emergency Commands

```bash
# Reset everything
just clean && just database::reset

# Stop all services
just down

# View all available commands
just --list
```

## Justfile Architecture

The project uses a hierarchical Justfile structure:
- **Main Justfile**: Entry point with command routing
- **.just/**: Utilities and common functions
- **tools/**: Domain-specific modules (docker, database, testing, demos)
- **apps/api/justfile**: Python-specific commands
- **apps/web/justfile**: Web-specific commands

Access module commands with `::` syntax: `just docker::up`, `just database::migrate`

All existing commands work unchanged. See [`docs/development/justfile-architecture.md`](docs/development/justfile-architecture.md) for details.

---

*This file is designed for rapid development. Quality gates and full testing come after feature implementation.*

## Documentation Directory

### Core Documentation
- **`docs/project-management/spec.md`** - Project requirements and success criteria
- **`docs/overview.md`** - Complete documentation map
- **`docs/architecture/architecture.md`** - Clean Architecture patterns and layer design

### Task & Project Management
- **`docs/project-management/roadmap.md`** - Development timeline and technical debt tracking
- **`docs/project-management/commits-plan.md`** - Detailed implementation phases
- **`docs/development/tasks-workflow.md`** - Task lifecycle from creation to completion
- **`docs/project-management/todo.md`** - Immediate tasks and notes
- **`docs/project-management/work-log.md`** - Append-only log of completed work
- **`docs/project-management/tasks/open/`** - Active tasks awaiting implementation
- **`docs/project-management/tasks/closed/`** - Completed tasks for archival

### Developer Guides  
- **`docs/development/local-setup.md`** - Environment setup and prerequisites
- **`docs/development/testing.md`** - Test strategy, fixtures, and coverage requirements
- **`docs/development/quality.md`** - Linting, type checking, and code standards
- **`docs/development/definition-of-done.md`** - Complete checklist for task completion
- **`docs/development/configuration.md`** - Hydra configuration management
- **`docs/development/alembic.md`** - Database migration workflows
- **`docs/development/refactoring.md`** - Safe code reorganization procedures

### API References
- **`docs/api/rest.md`** - REST endpoints with examples
- **`docs/api/graphql.md`** - GraphQL schema and queries

### Operations
- **`docs/operations/docker.md`** - Container build and security practices
- **`docs/operations/cli.md`** - Haven CLI tool for git diff generation

### When to Read Which Doc

1. **Starting fresh?** → `docs/local-setup.md` then `docs/spec.md`
2. **Adding a feature?** → `docs/architecture.md` then relevant API docs
3. **Managing tasks?** → `docs/tasks-workflow.md`
4. **Database changes?** → `docs/alembic.md`
5. **Cleaning up code?** → `docs/refactoring.md`
6. **Before committing?** → `docs/definition-of-done.md`
7. **Lost or confused?** → `docs/overview.md` for the complete map

**Remember**: Complete task → Run checks → Commit → Update work log → Next task. Never leave work uncommitted!

## Documentation Synchronization

After each commit, ensure all tracking files are synchronized:

### 1. Work Log (`docs/project-management/work-log.md`)
Append an entry with:
- **What was added/changed** - High-level description of the work done
- **How to see it** - URLs, commands, or file paths to view the changes
- **How to test it** - Commands to run tests or verify functionality
- **How to demo it** - Steps to demonstrate the new feature/fix

Example format:
```markdown
## 2025-07-16.0001 - Added GraphQL health check endpoint
**Added**: Basic GraphQL health check query returning service status
**See**: Visit http://api.haven.local/graphql and run `{ health { status } }`
**Test**: `just test tests/integration/test_graphql.py::test_health_query`
**Demo**: Start service with `just run`, open GraphiQL, execute health query
```

Use format `YYYY-MM-DD.NNNN` where NNNN is a zero-padded 4-digit sequence number starting from 0001 each day.

### 2. Todo List (`docs/project-management/todo.md`)
- Mark completed tasks with [x]
- Remove or strike through finished items
- Add any new tasks discovered during implementation
- Update priorities if needed

### 3. Roadmap (`docs/roadmap.md`)
- Mark milestones as completed
- Move items from "In Progress" to "Completed"
- Update sprint status if applicable
- Add any new backlog items discovered

### 4. Commits Plan (`docs/commits-plan.md`)
- Mark commits as completed if following the plan
- Note any deviations from the original plan
- Update remaining commit estimates

### 5. CLAUDE.md
- Add new workflows or commands created
- Update examples if APIs changed
- Add any new developer tips discovered

### Sync Checklist
```bash
# After each commit, verify:
□ docs/project-management/work-log.md has new entry
□ docs/project-management/todo.md reflects completed work
□ roadmap.md shows progress
□ commits-plan.md updated (if applicable)
□ CLAUDE.md has new workflows (if created)
□ Task moved to tasks/closed/ (if complete)
```

# Important!!!!

PLEASE DO NOT STOP AFTER FINISHING YOUR TASK. Your role is to implement all pending open tasks in this CLAUDE file, and in documents under the `./docs/` directory, particularly `./docs/project-management/{todo.md, tasks/*, roadmap.md}`. After finishing a commit, move on to the next one without prompting the user for any info.