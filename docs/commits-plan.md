maps the journey from skeleton to production-ready service.

---
# Implementation Storyboard

| Commit | Milestone |
|--------|-----------|
| 0 | Scaffold repo, pyproject, .gitignore, Justfile |
| 0.1 | Setup claude hooks |
| 0.2 | Quality baseline: Ruff + Pyright configs, pre-commit pipeline |
| 0.3 | Docs scaffold: `docs/*`|
| 0.4 | Local Docker-compose skeleton (Postgres service, health-check) |
| 1 | Hydra config tree + base settings dataclasses |
| 2 | Domain `Record` entity + unit tests |
| 3 | SQLAlchemy models, Postgres compose, Alembic baseline |
| 4 | Repository pattern + Unit-of-Work |
| 5 | Application services (CRUD) |
| 6 | REST routes + OpenAPI |
| 6.1 | `docs/api/rest.md` – endpoint list with example requests/responses |
| 7 | GraphQL schema/resolvers |
| 7.1 | `docs/api/graphql.md` – SDL, sample queries/mutations, pagination examples |
| 8 | Testing infra, fixtures, CI quality gate |
| 9 | MkDocs site, ADR template |
| 10 | Multi-stage Dockerfile, build script |
| 11 | Hardening, docs polish, version bump |
