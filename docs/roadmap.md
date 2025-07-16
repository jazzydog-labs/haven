# Haven - Development Roadmap

*Last updated: 2025-07-16*

This roadmap tracks planned features, technical debt, and incomplete items to maintain development flow and context.

---

## 🚀 Current Sprint (Active Development)

### ✅ Completed Major Milestones
- [x] **Core Infrastructure** (Commits 0-11) - Complete foundation with all APIs
- [x] **Monorepo Transformation** - Python backend + React frontend structure
- [x] **Git Diff Generation API** - Full repository diff analysis with HTML export
- [x] **Quality System** - Comprehensive testing, linting, type checking
- [x] **Production Readiness** - Docker containerization and deployment setup

### In Progress
- [x] **Script Organization** - Move complex logic from Justfile to dedicated shell scripts
- [ ] **Documentation Cleanup** - Update all docs to reflect completed work
- [ ] **Integration Test Fixes** - Resolve SQLAlchemy transaction management in tests

### Up Next

#### Containerization (3 Phases)

**Phase 1: Basic Containerization (✅ COMPLETED)**
- [x] **Docker Setup** - PostgreSQL and FastAPI in containers with docker-compose
- [x] **Hot Reload** - Ensure development workflow with code changes
- [x] **Just Commands** - Docker-aware commands in Justfile
- [x] **Dev Experience** - Fixed permissions, tool availability (diff2html)
- [x] **Documentation** - Updated CLAUDE.md with Docker workflow

**Phase 2: Developer Experience (Next Up)**
- [ ] **Override Config** - Development-specific docker-compose.override.yml
- [ ] **Migration Strategy** - Multiple approaches for database migrations
- [ ] **Troubleshooting** - Comprehensive guide for common issues

**Phase 3: Production-Like Environment (Enhancements)**
- [ ] **CORS/Domains** - Local domain setup to avoid CORS issues
- [ ] **HTTPS Setup** - Local SSL certificates for secure development
- [ ] **Reverse Proxy** - Production-like setup with Traefik/Caddy

#### Feature Development (After Containerization)
- [ ] **React Client Features** - Diff visualization interface
- [ ] **API Enhancements** - Additional diff analysis features
- [ ] **Shared SDK** - packages/sdk/ for API client library

---

## 📋 Backlog

### Frontend Development
- [ ] **Diff Visualization Interface** - React components for viewing diffs
- [ ] **Repository Browser** - Navigate commits and file changes
- [ ] **Search & Filter** - Find specific changes across history
- [ ] **Export Options** - PDF, markdown export of diff reports

### API Enhancements  
- [ ] **Advanced Diff Analysis** - File change metrics, complexity analysis
- [ ] **Repository Statistics** - Contributor stats, file evolution
- [ ] **Webhook Integration** - Real-time diff notifications
- [ ] **API Rate Limiting** - Protect against abuse

### Infrastructure & DevOps
- [ ] **Container Orchestration** - Production Docker setup with health checks
- [ ] **CI/CD Pipeline** - Automated testing and deployment
- [ ] **Monitoring Setup** - Prometheus/Grafana or similar
- [ ] **Backup Strategy** - Database backup and recovery

### Developer Experience
- [ ] **Shared SDK Package** - packages/sdk/ for API client
- [ ] **CLI Tool** - Command-line diff generation
- [ ] **VS Code Extension** - IDE integration for diff analysis
- [ ] **GitHub App** - Direct GitHub integration

---

## 🏗️ Technical Debt Tracker

### High Priority
- [ ] **Command Testing**: Verify all just commands work after monorepo restructure  
- [ ] **Documentation Sync**: Update all docs to reflect current architecture
- [ ] **Containerization**: Complete all three phases for better dev experience
- [ ] **Error Handling**: Standardize error responses across REST/GraphQL
- [ ] **API Documentation**: Auto-generate from OpenAPI/GraphQL schemas

### Medium Priority
- [ ] **Database Connection Pooling**: Configure proper async pooling for production
- [ ] **Logging Structure**: Implement structured JSON logging with correlation IDs
- [ ] **Rate Limiting**: Add before public API exposure
- [ ] **Metrics Collection**: OpenTelemetry integration for observability

### Low Priority  
- [ ] **Query Optimization**: Profile and optimize after load testing
- [ ] **Caching Layer**: Redis integration for hot paths
- [ ] **API Versioning**: Design strategy before v1.0
- [ ] **Performance Testing**: Load testing and benchmarking

---

## 🔮 Future Enhancements

### Infrastructure & Scaling
- [ ] Multi-tenancy support
- [ ] Event sourcing for audit trail
- [ ] Webhook system for integrations
- [ ] Horizontal scaling strategy
- [ ] Service mesh integration

### Features & Performance
- [ ] Advanced GraphQL features (subscriptions, dataloaders)
- [ ] Advanced monitoring dashboards
- [ ] Performance optimization pass

---

## ⚠️ Known Issues

### Development Environment
- **Issue**: Hot reload sometimes misses file changes
- **Workaround**: Restart with `just run`
- **Fix**: Investigate uvicorn watch configuration

### Testing
- **Issue**: Async test fixtures occasionally hang
- **Workaround**: Use `pytest-timeout`
- **Fix**: Review event loop handling in fixtures

### Documentation
- **Issue**: API docs drift from implementation
- **Workaround**: Manual updates required
- **Fix**: Auto-generate from OpenAPI/GraphQL schemas

---

## 📝 Decision Log

### Recent Decisions
1. **2025-07-16**: Chose Strawberry over Graphene for GraphQL (async native)
2. **2025-07-16**: Selected Chainguard base images (security focused)  
3. **2025-07-16**: Adopted Clean Architecture (maintainability)
4. **2025-07-16**: Implemented monorepo with Hatch workspaces (Python + TypeScript)
5. **2025-07-16**: Built git diff generation API with background processing
6. **2025-07-16**: Used React + TypeScript + Vite + Tailwind for frontend

### Pending Decisions
- [ ] Choose between Alembic auto-generate vs manual migrations
- [ ] Select monitoring solution (Datadog vs New Relic vs self-hosted)
- [ ] Decide on secret management approach

---

## 🎯 Success Metrics

### Sprint Goals
- [ ] All quality gates passing (lint, type, test)
- [ ] <30min bootstrap time for new developers
- [ ] 70% test coverage maintained
- [ ] Docker image <200MB

### Long-term Goals
- [ ] <100ms p95 response time
- [ ] 99.9% uptime SLA capability
- [ ] <5min deployment time
- [ ] Zero security vulnerabilities

---

## 🔄 Maintenance Notes

### Regular Tasks
- Update this roadmap with progress
- Review and prioritize technical debt
- Dependency updates and security patches
- Architecture review and optimization

### When Resuming Work
1. Check this roadmap for context
2. Review `todo.md` for immediate tasks
3. See `commits-plan.md` for implementation order
4. Run `just check` to ensure clean state

### Development Workflow
1. Pick the next task from "In Progress" or "Up Next"
2. Implement the feature/fix
3. Run quality gates (`just check`)
4. **Commit immediately with descriptive message**
5. Update task status in roadmap/todo
6. Move to the next task

**Never skip the commit step** - this ensures clean history and safe rollback points

---

*This document helps maintain momentum and context across development sessions. Update it regularly!*