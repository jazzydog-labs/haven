# Haven – Local Development Guide

*Last updated: 2025‑07‑15*

Welcome to Haven’s developer handbook for running everything on your own laptop—no external CI, no cloud credentials, just Docker and a shell.  Follow the steps below once; afterwards `just run` will bring the entire stack to life in under thirty seconds.

---

## 1  Prerequisites

* **macOS 12+** (Intel or Apple‑Silicon) or modern Linux.
* **Docker Desktop** (or Podman—even Docker‑Compose v2 CLI compatibility is all we need).
* **Python 3.12** (we recommend [https://github.com/pyenv/pyenv](https://github.com/pyenv/pyenv)).
* **Node 18+** (for Claude Code), installable with `nvm` or Homebrew.
* **Just** command‑runner—`brew install just` or grab a release binary from [https://just.systems](https://just.systems).

---

## 2  One‑Time Bootstrap

```bash
# 1. Clone the repository
 git clone git@github.com:jazzydog-labs/haven.git && cd haven

# 2. Install Python 3.12 and create a virtual env
 pyenv install 3.12.2    # skip if already installed
 pyenv local 3.12.2

# 3. Sync Python dependencies (Hatch + uv)
 curl -sSf https://install.hatch.pm | bash  # once per machine
 hatch env create
 hatch env run uv sync  # fast, deterministic

# 4. Install Claude Code globally
 npm install -g @anthropic-ai/claude-code

# 5. Copy the local config template
 cp conf/local/.env.example .env

# 6. Pull Docker images (Postgres + OTel collector)
 just db-up          # see § 3 for details
```

When the dust settles you’ll have:

* a Python virtual‑env with all dev dependencies,
* `postgres:16` running on port 5432 (data volume `haven_data`),
* an empty `.claude/settings.json` ready for permissive bootstrap,
* all **Justfile** tasks available in your `$PATH`.

---

## 3  The Docker Compose Stack

The compose file (`docker-compose.yaml`) defines three services:

* **`db`** – Postgres 16 with a durable volume mounted at `./.local/pgdata`.
~~* **`otel`** – Optional OpenTelemetry Collector on port 4317; disabled by default unless `OTEL_ENABLED=true` in your `.env`.~~ (skip for now)
* **`haven`** – Reserved for the app container during production builds; local development runs the app directly on your host via `uvicorn`.

Useful commands:

```bash
just db-up           # spin up Postgres (+ OTel if enabled)
just db-down         # stop and remove the compose stack
just db-migrate      # apply Alembic migrations to the running DB
```

All database credentials live in `.env` and are consumed by Hydra at runtime.

---

## 4  Running the Service

```bash
# Kick the tyres
just run             # starts uvicorn on http://localhost:8080

# Open http://localhost:8080/docs for Swagger
# Open http://localhost:8080/graphql for GraphiQL
```

Hot‑reload is on by default via `--reload`; edit a file and the server restarts in under a second.

---

## 5  Quality Gates on Your Laptop

The same gates CI will enforce can be run locally with one line:

```bash
just lint type test   # Ruff → Pyright → pytest‑cov (≥ 70 % or fail)
```

If any step fails, fix the warnings or add tests before committing—CI won’t be more forgiving.

---

## 6  Cheat‑Sheet of Everyday **Justfile** Targets

```text
install        – create/update the Hatch env (implicit in others)
run            – launch FastAPI + GraphQL with hot reload
lint           – ruff check .
type           – pyright --strict
lint-type      – ruff then pyright (shortcut)
test           – pytest --cov=haven --cov-fail-under=70
lint type test – all three quality gates in sequence
db-up          – docker compose up -d db [otel]
db-down        – docker compose down
db-migrate     – alembic upgrade head
docs           – mkdocs serve --dev-addr localhost:8001
demo           - runs all the demos
demo-*         - runs particular feature demo
claude         – interactive Claude Code session (bypass mode)
plan           – just claude "Plan: <task description>"
implement      – just claude "Implement pending tasks in todo.md"
```

Feel free to alias `just claude` to `cc` if you find yourself conversing with the bot regularly.

---

## 7  Tidying Up

To wipe everything:

```bash
just db-down     # stop containers
rm -rf .local/pgdata .mypy_cache .ruff_cache .pytest_cache .coverage
hatch env remove # remove the virtual env
```

You’ll be back to a pristine checkout, ready to onboard again or hand off to a teammate.

---