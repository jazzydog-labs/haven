# Generic Data-Store Microservice – Specification

## 1  Purpose & Scope
A self-contained microservice exposing both **REST-style** and **GraphQL** façades over a local **PostgreSQL** instance.  
It is intended for **local-first development workflows** where engineers need a robust persistence layer and strongly-typed APIs without standing up external infrastructure.

*Runs on* **`localhost:8080`** by default; configuration is fully environment-driven.

---

## 2  Technology Stack

| Concern | Choice | Notes |
|---------|--------|-------|
| Runtime | **Python 3.12** | Modern language features, long LTS horizon. |
| API     | **FastAPI 1.x** (async) | Automatic OpenAPI & Swagger docs. |
| GraphQL | **Strawberry 0.230** (or Ariadne) | Code-first schema, async resolvers. |
| ORM     | **SQLAlchemy 2.x (async)** + **asyncpg** | Unit-of-work friendly. |
| Validation | **Pydantic v2** | Used in both API layer and config models. |
| Config mgmt | **Hydra 1.3** | Hierarchical overrides, env injection. |
| Packaging | **pyproject.toml** (PEP 621) + **Hatch** | Reproducible, isolated builds. |
| Tooling | **Ruff**, **Pyright** | Lint + strict type-checking. |
| Testing | **pytest + pytest-cov** (≥ **70 %** line coverage gate). |
| Docs | **MkDocs** + *Material* theme | Auto-build via `just docs`. |
| Container | **Docker (Chainguard base)** | Distroless final stage, non-root UID. |
| Task runner | **Justfile** | One-liners for dev workflow. |

(Adapted from prior Symphony backend spec :contentReference[oaicite:0]{index=0})

---

## 3  Architectural Principles

1. **Clean Architecture layers** – Domain → Application → Infrastructure → Interface; dependencies point inward :contentReference[oaicite:1]{index=1}.  
2. **Async-first**: non-blocking I/O at DB and HTTP layers.  
3. **Repository + Unit-of-Work patterns** for persistence isolation and testability.  
4. **CQRS-friendly** application layer (commands & queries) – can be adopted incrementally.  
5. **12-Factor configuration** (§ 5).

---

## 4  Directory Layout

```
src/  
└── datastore_service/  
├── domain/ # Pure business logic, entities, VOs  
├── infrastructure/  
│ └── database/ # ORM models, SQLAlchemy engine  
├── application/ # Commands, queries, services  
├── api/  
│ ├── routes/ # FastAPI routers  
│ └── graphql/ # Strawberry schema & resolvers  
└── config/ # Hydra configs  
tests/ # Unit, integration, e2e  
docs/ # MkDocs site

```
This mirrors the proven layout in *architecture.md* while stripping domain-specific names :contentReference[oaicite:2]{index=2}.

---

## 5  Configuration

* **Hydra** root: `conf/{environment}/{component}.yaml`.  
* Sensitive settings (e.g., `DATABASE_URL`) come from environment variables; `conf/local` provides sane defaults for Docker compose.  
* Pydantic v2 models validate config at startup.

---

## 6  API Surface

| Layer | Path | Description |
|-------|------|-------------|
| REST  | `/records` | CRUD for a generic `Record` aggregate (UUID + JSON payload). |
| GraphQL | `/graphql` | Full query/mutation parity via Strawberry GraphiQL UI. |
| Docs | `/docs` Swagger, `/redoc`, `/graphql` GraphiQL interactive IDE. |

---

## 7  Quality Gates

* `just lint` → Ruff must pass with **zero** warnings.  
* `just type` → Pyright in **strict** mode.  
* `just test` → pytest with `--cov=datastore_service --cov-fail-under=70`.  
* Pre-commit hook runs **lint → type → test** cascade.

(Testing breakdown derived from earlier backend guidance :contentReference[oaicite:3]{index=3})

---

## 8  Operational Workflows (Justfile excerpts)

| Command | Action |
|---------|--------|
| `just install` | `uv sync` + `hatch env create` |
| `just db-up` / `db-down` | Bring Postgres (compose) up/down |
| `just db-migrate` | Run Alembic `upgrade head` |
| `just run` | `uvicorn datastore_service.main:app --reload --port 8080` |
| `just lint / type / test` | Quality checks |
| `just docs` | Live-reload MkDocs site |
| `just build` | Multi-arch Docker buildx (Chainguard) |

Recipes echo patterns in Symphony’s reference Justfile :contentReference[oaicite:4]{index=4}.

---

## 9  Containerization & Security

* **Multi-stage Dockerfile**  
  * Stage 1: Chainguard `python:latest-dev` builder (installs dependencies).  
  * Stage 2: Chainguard `python:latest` distroless runtime, copy venv, non-root UID, tini entrypoint.
* SBOM emitted via **apko**; recommend Trivy scan in CI (outside current scope).

---

## 10  Testing Strategy

| Tier | Focus | Tools |
|------|-------|-------|
| Unit (≈ 60 %) | Domain logic, helpers | pytest |
| Integration (≈ 30 %) | Repositories ↔ Postgres, API client | pytest-asyncio, httpx |
| E2E (≈ 10 %) | Full request → DB → response | Docker-compose test stack |

Coverage target aggregated to **≥ 70 %** across all tiers.

---

## 11  Documentation

* **MkDocs-Material** with `mkdocstrings[python]` to auto-render API refs.  
* Deployment preview via `just docs` (serves on `localhost:8001`).  
* ADRs stored under `docs/adr/` to capture architectural decisions.

---

## 12  Success Criteria

1. **Bootstrap ≤ 30 min**: `just install && just db-up && just run` yields live service and docs.  
2. **Green quality gate**: lint, type, tests all pass on every commit.  
3. **70 %+ coverage** enforced; failing gate blocks merge.  
4. **Swagger & GraphiQL** both functional out of the box.  
5. **Docker image < 200 MB**, CVE scan “critical=0”.

---

## 13  Out of Scope (v1)

* Authentication/authorization  
* Horizontal sharding, read replicas  
* Event sourcing or message queues  
* Production CI/CD pipelines

The design, however, leaves clear extension points for each.
