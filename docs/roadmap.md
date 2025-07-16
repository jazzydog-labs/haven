# Haven - Development Roadmap

*Last updated: 2025-07-16*

This roadmap tracks planned features, technical debt, and incomplete items to maintain development flow and context.

---

## 🚀 Current Sprint (Active Development)

### In Progress
- [ ] Core project scaffolding (Commit 0)
  - [x] Documentation structure
  - [ ] Python project setup (pyproject.toml)
  - [ ] Quality tooling configuration
  - [ ] Docker compose for PostgreSQL

### Up Next
- [ ] Hydra configuration setup (Commit 1)
- [ ] Domain entity implementation (Commit 2)
- [ ] Database layer with SQLAlchemy (Commit 3)

---

## 📋 Backlog (Next 4 Weeks)

### Week 1-2: Core Infrastructure
- [ ] Repository pattern implementation
- [ ] Application services layer
- [ ] REST API with FastAPI
- [ ] GraphQL schema with Strawberry

### Week 3-4: Quality & Operations
- [ ] Comprehensive test suite (70% coverage)
- [ ] CI/CD pipeline setup
- [ ] Docker containerization
- [ ] Production hardening

---

## 🏗️ Technical Debt Tracker

### High Priority
- [ ] **Database Connection Pooling**: Need to configure proper async pooling
- [ ] **Error Handling**: Standardize error responses across REST/GraphQL
- [ ] **Logging Structure**: Implement structured JSON logging

### Medium Priority
- [ ] **API Versioning**: Design strategy before v1.0
- [ ] **Rate Limiting**: Add before public exposure
- [ ] **Metrics Collection**: OpenTelemetry integration

### Low Priority
- [ ] **Query Optimization**: Profile and optimize after load testing
- [ ] **Caching Layer**: Redis integration for hot paths
- [ ] **API Documentation**: Auto-generate from code

---

## 🔮 Future Enhancements (3+ Months)

### Q2 2025
- [ ] Multi-tenancy support
- [ ] Event sourcing for audit trail
- [ ] Webhook system for integrations
- [ ] Advanced GraphQL features (subscriptions, dataloaders)

### Q3 2025
- [ ] Horizontal scaling strategy
- [ ] Service mesh integration
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

## 📅 Milestone Timeline

```
2025-07-16: Project initialized
2025-07-20: Core infrastructure complete (target)
2025-07-27: API layer functional (target)
2025-08-03: Testing and quality complete (target)
2025-08-10: Production ready v0.1.0 (target)
```

---

## 🔄 Maintenance Notes

### Regular Tasks
- **Weekly**: Update this roadmap with progress
- **Bi-weekly**: Review and prioritize technical debt
- **Monthly**: Dependency updates and security patches
- **Quarterly**: Architecture review and optimization

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