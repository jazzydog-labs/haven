# Haven - Current Tasks & Immediate Notes

*Updated: 2025-07-16*

This file tracks immediate tasks and notes. For completed work, see `work-log.md`.

---

## 🎯 Current Focus: Frontend Development Phase

### 🚀 WHAT TO WORK ON NEXT (Priority Order)

All previous phases are now complete! Next priorities:

1. **Frontend Development** (Priority 3):
   - [ ] CRUD Frontend for Records (`tasks/open/crud-frontend-records.md`)
   - [ ] Frontend-Backend Sync Workflow (`tasks/open/frontend-backend-sync-workflow.md`)

2. **Containerization Phase 3** (Enhancements):
   - [ ] Set up local HTTPS (`tasks/open/local-https-setup.md`)
   - [ ] Create production-like environment (`tasks/open/production-like-local-env.md`)

### Documentation Updates (In Progress)
- [x] Create work-log.md from completed development 
- [x] Update this todo.md to remove completed items
- [x] Update docs/roadmap.md to reflect completed milestones
- [x] Update docs/commits-plan.md to mark commits 0-11 as done
- [x] Update docs/overview.md with new scripts organization

### Comprehensive Just Command Testing
All commands need verification after monorepo restructure:

**Core Commands**
- [ ] `just bootstrap` - Full environment setup
- [ ] `just db-up` - PostgreSQL startup  
- [ ] `just run` - API server with hot reload
- [ ] `just clean` - Environment cleanup
- [ ] `just down` - Stop all services

**Python Development**
- [ ] `just test-python` - Run Python test suite
- [ ] `just lint-python` - Python linting with Ruff
- [ ] `just type-python` - Type checking with Pyright
- [ ] `just format-python` - Code formatting
- [ ] `just check-python` - All Python quality gates

**TypeScript Development** 
- [ ] `just test-web` - Run React/TypeScript tests
- [ ] `just lint-web` - TypeScript linting with ESLint
- [ ] `just type-web` - TypeScript type checking
- [ ] `just format-web` - Code formatting with Prettier
- [ ] `just check-web` - All TypeScript quality gates

**Utilities**
- [ ] `just docs` - Build MkDocs documentation
- [ ] `just demo-diff-generation` - Full repository diff demo
- [ ] `just db-console` - Database console access
- [ ] `just shell` - Python REPL with app context
- [ ] `just logs` - View application logs

### Fix Issues
- [ ] Address any failing just commands discovered during testing

---

## 📋 Immediate Next Steps

### Priority 1: Foundation & Organization ✅ (COMPLETED)
1. ✅ **Single Command Commit Viewer** - `just demo-commits` now handles server startup automatically
2. ✅ **Reorganize Project Structure** - Cleaned up docs and configs
3. ✅ **Complete Documentation Updates** - All planning docs reflect current state
4. ✅ **Test All Commands** - Fixed missing commands (down, check-python, check-web)

### Priority 2: Development Infrastructure ✅ (MOSTLY COMPLETE)  
4. ✅ **Modularize Justfiles** - Split into package-specific modules with full backward compatibility
5. **Add Demo Commands** - Ensure all worklog entries have demo commands (see `tasks/open/worklog-demo-commands.md`)

### Priority 2.5: ✅ Containerization - Phase 1 (COMPLETED)
**Completed tasks:**
- [x] Containerize PostgreSQL and FastAPI services (see `tasks/closed/containerize-services.md`)
- [x] Containerize FastAPI with hot-reload support (see `tasks/closed/containerize-api-service.md`)
- [x] Add Docker commands to Justfile (see `tasks/closed/add-docker-justfile-commands.md`)
- [x] Resolve developer experience issues (see `tasks/closed/container-dev-experience.md`)
- [x] Update containerization docs (see `tasks/closed/update-containerization-docs.md`)

### Priority 2.6: ✅ Containerization - Phase 2 (COMPLETED)
**Completed tasks:**
- [x] Create docker-compose.override.yml (see `tasks/closed/create-dev-overrides.md`)
- [x] Implement migration strategies (see `tasks/closed/implement-migration-strategy.md`)
- [x] Create troubleshooting guide (see `tasks/closed/container-troubleshooting-guide.md`)

### Priority 2.7: Containerization - Phase 3 (Enhancements)
**Optional improvements (can be done in parallel):**
- [ ] Configure CORS and local domains (see `tasks/open/local-cors-and-domains.md`)
- [ ] Set up local HTTPS (see `tasks/open/local-https-setup.md`)
- [ ] Create production-like environment (see `tasks/open/production-like-local-env.md`)

### Priority 3: Frontend Development
6. **CRUD Frontend for Records** - Complete UI for Records management (see `tasks/open/crud-frontend-records.md`)
7. **Frontend-Backend Sync Workflow** - Automated type generation and API sync (see `tasks/open/frontend-backend-sync-workflow.md`)

### Priority 4: Next Development Phase
8. **Fix Any Issues** - Address command failures or configuration problems  
9. **Begin Next Development Phase** - Start implementing new features

### Active Tasks in `tasks/open/` (By Priority)

**Development Infrastructure (One Task Remaining):**
- `worklog-demo-commands.md` - Add demo commands for all worklog entries

**Containerization Phase 3 (Enhancements):**
- `local-cors-and-domains.md` - CORS and custom domain configuration
- `local-https-setup.md` - HTTPS development environment
- `production-like-local-env.md` - Full production-like setup with reverse proxy

**Frontend Development (Priority 3):**
- `crud-frontend-records.md` - Complete CRUD UI for Records management
- `frontend-backend-sync-workflow.md` - Automated type generation from backend
- `production-like-local-env.md` - Full production-like setup with reverse proxy

---

## 🔄 Development Workflow

When resuming work:
1. Check this `todo.md` for immediate tasks
2. Review docs for implementation strategy:
   - `work-log.md` - What's been completed
   - `docs/roadmap.md` - Current sprint and backlog
   - `docs/commits-plan.md` - Implementation order
   - `docs/architecture.md` - Design patterns to follow
   - `CLAUDE.md` - Quick reference and doc directory
3. Continue from the next uncompleted task
4. **Complete the task fully**
5. Ensure all quality gates pass (see `docs/definition-of-done.md`)
6. **Commit immediately with clear message**
7. Move to the next task

**Critical**: Never batch multiple tasks into one commit. Each logical unit of work should be committed separately for clear history and safe rollbacks.

---

## 📝 Notes & Context

### Project Status
- **Phase Completed**: Monorepo transformation with Python API + React client
- **Current State**: All core functionality operational, need comprehensive testing
- **Next Phase**: Documentation cleanup, then continue feature development

### Key Achievements
- ✅ FastAPI REST + Strawberry GraphQL APIs
- ✅ Git diff generation with HTML export  
- ✅ Monorepo with Hatch workspaces
- ✅ React client with TypeScript + Tailwind
- ✅ Comprehensive testing and quality gates
- ✅ Production-ready containerization

### Architecture Notes
- **Backend**: apps/api/ with Clean Architecture patterns
- **Frontend**: apps/web/ with React + TypeScript + Vite
- **Shared**: packages/ for future SDK and shared components
- **Config**: Hydra for multi-environment configuration
- **Database**: PostgreSQL with SQLAlchemy 2.x async

---

*Keep this file updated as you complete tasks. Move completed items to work-log.md periodically.*