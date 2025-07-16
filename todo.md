# Haven - Current Tasks & Immediate Notes

*Updated: 2025-07-16*

This file tracks immediate tasks and notes. For completed work, see `work-log.md`.

---

## 🎯 Current Focus: Documentation & Testing Phase

### 🚀 WHAT TO WORK ON NEXT (Priority Order)

1. **Foundation Tasks** (Do these first - they affect everything else):
   - [ ] Reorganize project structure (`tasks/open/reorganize-project-structure.md`)
   - [ ] Test all Just commands after monorepo restructure (list below)
   - [ ] Complete documentation sync (this task is in progress)

2. **Containerization Phase 2** (After foundation tasks):
   - [ ] Create docker-compose.override.yml (`tasks/open/create-dev-overrides.md`)
   - [ ] Implement migration strategies (`tasks/open/implement-migration-strategy.md`)
   - [ ] Create troubleshooting guide (`tasks/open/container-troubleshooting-guide.md`)

3. **Development Infrastructure** (Can be done in parallel):
   - [ ] Modularize Justfiles (`tasks/open/modular-justfiles.md`)
   - [ ] Add demo commands for all worklog entries (`tasks/open/worklog-demo-commands.md`)

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

### Priority 1: Foundation & Organization (Prerequisites)
1. ✅ **Single Command Commit Viewer** - `just demo-commits` now handles server startup automatically
2. **Reorganize Project Structure** - Clean up docs and configs (see `tasks/open/reorganize-project-structure.md`)
3. **Complete Documentation Updates** - Update all planning docs to reflect current state
4. **Test All Commands** - Systematically verify every just command works

### Priority 2: Development Infrastructure  
4. **Modularize Justfiles** - Break down justfile into package-specific modules (see `tasks/open/modular-justfiles.md`)
5. **Add Demo Commands** - Ensure all worklog entries have demo commands (see `tasks/open/worklog-demo-commands.md`)

### Priority 2.5: ✅ Containerization - Phase 1 (COMPLETED)
**Completed tasks:**
- [x] Containerize PostgreSQL and FastAPI services (see `tasks/closed/containerize-services.md`)
- [x] Containerize FastAPI with hot-reload support (see `tasks/closed/containerize-api-service.md`)
- [x] Add Docker commands to Justfile (see `tasks/closed/add-docker-justfile-commands.md`)
- [x] Resolve developer experience issues (see `tasks/closed/container-dev-experience.md`)
- [x] Update containerization docs (see `tasks/closed/update-containerization-docs.md`)

### Priority 2.6: Containerization - Phase 2 (Next Up)
**Ready to implement:**
- [ ] Create docker-compose.override.yml (see `tasks/open/create-dev-overrides.md`)
- [ ] Implement migration strategies (see `tasks/open/implement-migration-strategy.md`)
- [ ] Create troubleshooting guide (see `tasks/open/container-troubleshooting-guide.md`)

### Priority 2.7: Containerization - Phase 3 (Enhancements)
**Optional improvements (can be done in parallel):**
- [ ] Configure CORS and local domains (see `tasks/open/local-cors-and-domains.md`)
- [ ] Set up local HTTPS (see `tasks/open/local-https-setup.md`)
- [ ] Create production-like environment (see `tasks/open/production-like-local-env.md`)

### Priority 3: Next Development Phase
6. **Fix Any Issues** - Address command failures or configuration problems  
7. **Begin Next Development Phase** - Start implementing new features

### Active Tasks in `tasks/open/` (By Priority)

**Foundation Tasks (Do First):**
- `reorganize-project-structure.md` - **HIGH PRIORITY** - Foundation for all other work
- `modular-justfiles.md` - Depends on project structure being clean
- `worklog-demo-commands.md` - Can be done in parallel with structure work

**Containerization Phase 2 (Ready to Implement):**
- `create-dev-overrides.md` - Development environment config for hot-reload
- `implement-migration-strategy.md` - Multiple migration approaches
- `container-troubleshooting-guide.md` - Troubleshooting documentation

**Containerization Phase 3 (Enhancements):**
- `local-cors-and-domains.md` - CORS and custom domain configuration
- `local-https-setup.md` - HTTPS development environment
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