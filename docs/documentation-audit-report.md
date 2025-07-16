# Documentation Audit Report

## Summary

- **Files Scanned**: 71
- **Files with Issues**: 65
- **Total Issues**: 946

### Issues by Type

- **Invalid Paths**: 646
- **Invalid Commands**: 188
- **Broken Links**: 33
- **Localhost Urls**: 79

## Detailed Issues

### CLAUDE.md

- **Line 81**: Invalid Path - `docs/architecture.md`
- **Line 173**: Invalid Path - `docs/quality.md`
- **Line 173**: Invalid Path - `docs/definition-of-done.md`
- **Line 304**: Invalid Path - `docs/local-setup.md`
- **Line 304**: Invalid Path - `docs/spec.md`
- **Line 306**: Invalid Path - `docs/tasks-workflow.md`
- **Line 307**: Invalid Path - `docs/alembic.md`
- **Line 308**: Invalid Path - `docs/refactoring.md`
- **Line 334**: Invalid Path - `YYYY-MM-DD.NNNN`
- **Line 342**: Invalid Path - `docs/roadmap.md`
- **Line 348**: Invalid Path - `docs/commits-plan.md`
- **Line 14**: Invalid Path - `//web.haven.local`
- **Line 15**: Invalid Path - `//api.haven.local/docs`
- **Line 16**: Invalid Path - `//api.haven.local/graphql`
- **Line 46**: Invalid Path - `roadmap/todo`
- **Line 70**: Invalid Path - `tests/test_api.py`
- **Line 100**: Invalid Path - `tasks/open/feature-name.md`
- **Line 109**: Invalid Path - `docs/workflow-name.md`
- **Line 111**: Invalid Path - `Tools/Commands`
- **Line 119**: Invalid Path - `src/interface/api/routes.py`
- **Line 125**: Invalid Path - `tests/interface/api/test_routes.py`
- **Line 130**: Invalid Path - `src/interface/graphql/schema.py`
- **Line 143**: Invalid Path - `src/domain/models.py`
- **Line 173**: Invalid Path - `linting/typing`
- **Line 227**: Invalid Path - `Python/Node`
- **Line 320**: Invalid Path - `added/changed`
- **Line 323**: Invalid Path - `feature/fix`
- **Line 330**: Invalid Path - `tests/integration/test_graphql.py`
- **Line 366**: Invalid Path - `tasks/closed/`
- **Line 371**: Invalid Path - `/docs/project-management/`
- **Line 37**: Invalid Command - `just database::up     # Start PostgreSQL`
- **Line 37**: Invalid Command - `just testing::fast    # Run unit tests only (quick feedback)`
- **Line 62**: Invalid Command - `just api::add-entity User`
- **Line 62**: Invalid Command - `just database::make "add_users_table" && just database::migrate`
- **Line 142**: Invalid Command - `just database::make "add_status_to_items"`
- **Line 149**: Invalid Command - `just database::console`
- **Line 149**: Invalid Command - `just shell`
- **Line 202**: Invalid Command - `just docker::up-d      # Start all services in background`
- **Line 202**: Invalid Command - `just docker::down      # Stop all services`
- **Line 202**: Invalid Command - `just docker::logs api  # View API logs`
- **Line 202**: Invalid Command - `just docker::shell     # Shell into API container`
- **Line 202**: Invalid Command - `just database::migrate-docker             # Run migrations in Docker`
- **Line 202**: Invalid Command - `just database::make-docker "add_users"   # Create migration in Docker`
- **Line 202**: Invalid Command - `just database::console-docker             # Database console via Docker`
- **Line 202**: Invalid Command - `just docker::test      # Run tests in container`
- **Line 202**: Invalid Command - `just docker::lint      # Run linting in container`
- **Line 202**: Invalid Command - `just docker::type-check # Type checking in container`
- **Line 202**: Invalid Command - `just docker::ps        # Show running containers`
- **Line 202**: Invalid Command - `just docker::rebuild   # Rebuild containers`
- **Line 202**: Invalid Command - `just docker::reset     # Full reset (data loss!)`
- **Line 241**: Invalid Command - `just --list`
- **Line 261**: Invalid Command - `just docker::up`
- **Line 261**: Invalid Command - `just database::migrate`

### README.md

- **Line 3**: Invalid Path - `//github.com/jazzydog-labs/haven/actions/workflows/ci.yml/badge.svg`
- **Line 3**: Invalid Path - `//github.com/jazzydog-labs/haven/actions/workflows/ci.yml`
- **Line 4**: Invalid Path - `//img.shields.io/badge/python-3.12`
- **Line 4**: Invalid Path - `//www.python.org/downloads/`
- **Line 5**: Invalid Path - `//img.shields.io/badge/License-MIT-yellow.svg`
- **Line 5**: Invalid Path - `//opensource.org/licenses/MIT`
- **Line 6**: Invalid Path - `//img.shields.io/badge/code`
- **Line 6**: Invalid Path - `//github.com/astral-sh/ruff`
- **Line 14**: Invalid Path - `async/await`
- **Line 24**: Invalid Path - `//github.com/jazzydog-labs/haven.git`
- **Line 41**: Invalid Path - `//localhost`
- **Line 41**: Invalid Path - `8080/docs`
- **Line 42**: Invalid Path - `8080/graphql`
- **Line 43**: Invalid Path - `8080/health`
- **Line 49**: Invalid Path - `src/haven/`
- **Line 67**: Invalid Path - `//github.com/casey/just`
- **Line 86**: Invalid Path - `tests/unit/domain/test_record.py`
- **Line 111**: Invalid Path - `8080/api/v1/records`
- **Line 112**: Invalid Path - `application/json`
- **Line 144**: Invalid Path - `//jazzydog-labs.github.io/haven`
- **Line 147**: Invalid Path - `docs/architecture.md`
- **Line 148**: Invalid Path - `docs/local-setup.md`
- **Line 150**: Invalid Path - `docs/testing.md`
- **Line 151**: Invalid Path - `docs/deployment.md`
- **Line 168**: Invalid Path - `//fastapi.tiangolo.com/`
- **Line 169**: Invalid Path - `//strawberry.rocks/`
- **Line 170**: Invalid Path - `//www.sqlalchemy.org/`
- **Line 171**: Invalid Path - `//pydantic-docs.helpmanual.io/`
- **Line 172**: Invalid Path - `//hydra.cc/`
- **Line 71**: Invalid Command - `just --list      # Show all available commands`
- **Line 71**: Invalid Command - `just docs-serve  # Preview documentation locally`
- **Line 71**: Invalid Command - `just docker-build # Build Docker image`
- **Line 81**: Invalid Command - `just test-file tests/unit/domain/test_record.py`
- **Line 81**: Invalid Command - `just testing::coverage`
- **Line 147**: Broken Link - [Architecture Overview](docs/architecture.md)
- **Line 148**: Broken Link - [Local Setup Guide](docs/local-setup.md)
- **Line 150**: Broken Link - [Testing Guide](docs/testing.md)
- **Line 151**: Broken Link - [Deployment Guide](docs/deployment.md)
- **Line 41**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 42**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 43**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 111**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 116**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`

### apps/api/README.md

- **Line 9**: Invalid Path - `async/await`
- **Line 25**: Invalid Path - `//localhost`
- **Line 25**: Invalid Path - `8080/docs`
- **Line 26**: Invalid Path - `8080/graphql`
- **Line 27**: Invalid Path - `8080/health`
- **Line 61**: Invalid Path - `8080/api/v1/records`
- **Line 62**: Invalid Path - `application/json`
- **Line 48**: Invalid Command - `just type-python      # Type checking`
- **Line 48**: Invalid Command - `just format-python    # Format code`
- **Line 25**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 26**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 27**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 61**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 66**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`

### apps/web/README.md

- **Line 25**: Invalid Path - `//localhost`
- **Line 61**: Invalid Path - `8080/api/`
- **Line 62**: Invalid Path - `8080/graphql`
- **Line 25**: Localhost Url - `http://web.haven.local` → `http://web.haven.local`
- **Line 25**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 61**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 62**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`

### docs/api/diff-generation.md

- **Line 95**: Invalid Path - `scripts/demo-diff-generation.py`
- **Line 29**: Invalid Path - `//localhost`
- **Line 29**: Invalid Path - `8080/api/v1/diffs/generate`
- **Line 30**: Invalid Path - `application/json`
- **Line 42**: Invalid Path - `/api/v1/diffs/generate`
- **Line 64**: Invalid Path - `/api/v1/diffs/status/`
- **Line 79**: Invalid Path - `/api/v1/diffs/`
- **Line 17**: Invalid Command - `just demo-diff-generation`
- **Line 29**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`

### docs/api/graphql.md

- **Line 154**: Invalid Path - `conf/.../graphql.yaml`
- **Line 187**: Invalid Path - `tests/integration/api/`
- **Line 195**: Invalid Path - `create/update`

### docs/api/index.md

- **Line 10**: Invalid Path - `request/response`
- **Line 19**: Invalid Path - `//localhost`
- **Line 19**: Invalid Path - `8080/api/v1`
- **Line 24**: Invalid Path - `8080/api/v1/records`
- **Line 41**: Invalid Path - `8080/graphql`
- **Line 94**: Invalid Path - `requests/hour`
- **Line 95**: Invalid Path - `queries/hour`
- **Line 112**: Invalid Path - `/api/v1/`
- **Line 112**: Invalid Path - `/api/v2/`
- **Line 19**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 24**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 41**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`

### docs/api/openapi.md

- **Line 66**: Invalid Path - `src/haven/interface/api/app.py`
- **Line 8**: Invalid Path - `//localhost`
- **Line 8**: Invalid Path - `8080/docs`
- **Line 11**: Invalid Path - `8080/redoc`
- **Line 15**: Invalid Path - `8080/openapi.json`
- **Line 23**: Invalid Path - `Request/response`
- **Line 36**: Invalid Path - `openapitools/openapi-generator-cli`
- **Line 61**: Invalid Path - `Import/Export`
- **Line 80**: Invalid Path - `//opensource.org/licenses/MIT`
- **Line 96**: Invalid Path - `/api/v1/records`
- **Line 117**: Invalid Path - `application/json`
- **Line 119**: Invalid Path - `/components/schemas/RecordListResponseDTO`
- **Line 149**: Invalid Path - `stoplight/spectral-cli`
- **Line 158**: Invalid Path - `//fastapi.tiangolo.com/`
- **Line 159**: Invalid Path - `//swagger.io/specification/`
- **Line 8**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 8**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 11**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 11**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 15**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 40**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 46**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 55**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 62**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 137**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 140**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`

### docs/api/rest.md

- **Line 220**: Invalid Path - `value_error.missing`
- **Line 292**: Invalid Path - `record.created`
- **Line 12**: Invalid Path - `//localhost`
- **Line 12**: Invalid Path - `8080/api/v1`
- **Line 15**: Invalid Path - `/api/v1`
- **Line 32**: Invalid Path - `application/json`
- **Line 89**: Invalid Path - `/api/v1/records`
- **Line 117**: Invalid Path - `/api/v1/records/`
- **Line 196**: Invalid Path - `/data/key`
- **Line 197**: Invalid Path - `/data/new_field`
- **Line 308**: Invalid Path - `8080/api/v1/records`
- **Line 313**: Invalid Path - `8080/api/v1/records/550e8400-e29b-41d4-a716-446655440000`
- **Line 342**: Invalid Command - `just docs`
- **Line 12**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 308**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 313**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 320**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 332**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`

### docs/architecture/architecture.md

- **Line 38**: Invalid Path - `src/domain/`
- **Line 47**: Invalid Path - `src/domain/entities/record.py`
- **Line 56**: Invalid Path - `src/application/`
- **Line 64**: Invalid Path - `src/application/use_cases/create_record.py`
- **Line 70**: Invalid Path - `src/infrastructure/`
- **Line 79**: Invalid Path - `src/infrastructure/database/repositories/record_repository.py`
- **Line 84**: Invalid Path - `src/interface/`
- **Line 93**: Invalid Path - `src/interface/api/routes/records.py`
- **Line 133**: Invalid Path - `read/write`

### docs/architecture/domain-glossary.md

- **Line 31**: Invalid Path - `jazzydog-labs/haven`
- **Line 95**: Invalid Path - `text/content`
- **Line 147**: Invalid Path - `reviewed/needs`
- **Line 153**: Invalid Path - `Edit/delete`
- **Line 164**: Invalid Path - `Add/remove`
- **Line 173**: Invalid Path - `/api/v1/repositories`
- **Line 179**: Invalid Path - `id/sync`
- **Line 181**: Invalid Path - `/api/v1/commits`
- **Line 184**: Invalid Path - `id/diff`
- **Line 186**: Invalid Path - `/api/v1/reviews`
- **Line 193**: Invalid Path - `/api/v1/comments`
- **Line 200**: Invalid Path - `/api/v1/users`

### docs/changelog.md

- **Line 5**: Invalid Path - `//keepachangelog.com/en/1.0.0/`
- **Line 6**: Invalid Path - `//semver.org/spec/v2.0.0.html`
- **Line 17**: Invalid Path - `CI/CD`
- **Line 44**: Invalid Path - `//github.com/jazzydog-labs/haven/compare/main...HEAD`

### docs/contributing.md

- **Line 53**: Invalid Path - `//github.com/your-username/haven.git`
- **Line 57**: Invalid Path - `//github.com/jazzydog-labs/haven.git`
- **Line 79**: Invalid Path - `feature/your-feature-name`
- **Line 93**: Invalid Command - `just testing::coverage`
- **Line 26**: Broken Link - [roadmap](roadmap.md)

### docs/development/alembic.md

- **Line 16**: Invalid Path - `sqlalchemy.ext.asyncio`
- **Line 33**: Invalid Path - `env.py`
- **Line 39**: Invalid Path - `{YYYYMMDD}_{NN}_{slug}.py`
- **Line 57**: Invalid Path - `models.py`
- **Line 23**: Invalid Path - `src/haven/infrastructure/database/`
- **Line 47**: Invalid Path - `versions/20250715_02_add_tag_column_to_record.py`
- **Line 140**: Invalid Path - `migrations/archive/`
- **Line 195**: Invalid Path - `CI/CD`
- **Line 234**: Invalid Path - `//alembic.sqlalchemy.org/en/latest/branches.html`
- **Line 234**: Invalid Path - `//alembic.sqlalchemy.org/en/latest/cookbook.html`
- **Line 45**: Invalid Command - `just database::make "add tag column to record"`
- **Line 164**: Invalid Command - `just database::downgrade 1`
- **Line 58**: Invalid Command - `just database::make "<message>"`
- **Line 71**: Invalid Command - `just database::make`
- **Line 152**: Invalid Command - `just database::migrate-prod`
- **Line 191**: Invalid Command - `just database::migrate-offline`

### docs/development/configuration.md

- **Line 8**: Invalid Path - `cache/redis.yaml`
- **Line 47**: Invalid Path - `haven.config.settings.AppSettings`
- **Line 56**: Invalid Path - `database/postgres.yaml`
- **Line 109**: Invalid Path - `redis.yaml`
- **Line 109**: Invalid Path - `local.yaml`
- **Line 110**: Invalid Path - `defaults.yaml`
- **Line 40**: Invalid Path - `environment/local`
- **Line 40**: Invalid Path - `database/postgres`
- **Line 40**: Invalid Path - `logging/default`
- **Line 59**: Invalid Path - `//haven`
- **Line 59**: Invalid Path - `5432/haven`
- **Line 74**: Invalid Path - `environment/test.yaml`
- **Line 146**: Invalid Path - `//hydra.cc/docs/intro/`

### docs/development/cors-and-domains.md

- **Line 57**: Invalid Path - `127.0.0.1 api.haven.local`
- **Line 58**: Invalid Path - `127.0.0.1 app.haven.local`
- **Line 59**: Invalid Path - `127.0.0.1 haven.local`
- **Line 20**: Invalid Path - `//localhost`
- **Line 23**: Invalid Path - `//app.haven.local`
- **Line 24**: Invalid Path - `//api.haven.local`
- **Line 34**: Invalid Path - `//your-custom-origin.com`
- **Line 53**: Invalid Path - `/scripts/setup-local-domains.sh`
- **Line 63**: Invalid Path - `macOS/Linux`
- **Line 76**: Invalid Path - `8080/docs`
- **Line 77**: Invalid Path - `8080/graphql`
- **Line 96**: Invalid Path - `//haven.local`
- **Line 97**: Invalid Path - `//haven.local/api`
- **Line 98**: Invalid Path - `//haven.local/graphql`
- **Line 99**: Invalid Path - `//haven.local/docs`
- **Line 133**: Invalid Path - `//127.0.0.1`
- **Line 161**: Invalid Path - `/operations/production-setup.md`
- **Line 160**: Broken Link - [Local HTTPS Setup](local-https-setup.md)
- **Line 161**: Broken Link - [Production Environment](../operations/production-setup.md)
- **Line 20**: Localhost Url - `http://web.haven.local` → `http://web.haven.local`
- **Line 21**: Localhost Url - `http://localhost:5173` → `http://haven.local:5173`
- **Line 22**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 33**: Localhost Url - `http://web.haven.local` → `http://web.haven.local`
- **Line 42**: Localhost Url - `http://web.haven.local` → `http://web.haven.local`
- **Line 42**: Localhost Url - `http://localhost:5173` → `http://haven.local:5173`

### docs/development/definition-of-done.md

- **Line 143**: Invalid Path - `todo.md`
- **Line 143**: Invalid Path - `docs/roadmap.md`
- **Line 144**: Invalid Path - `feature/fix`
- **Line 117**: Invalid Command - `just docs   # Build documentation`
- **Line 34**: Invalid Command - `just docs`

### docs/development/demo-commands.md

- **Line 115**: Invalid Path - `justfile.demos`
- **Line 147**: Invalid Path - `/operations/container-troubleshooting.md`
- **Line 81**: Invalid Command - `just demos::health`
- **Line 81**: Invalid Command - `just demos::api`
- **Line 93**: Invalid Command - `just demos::all`
- **Line 102**: Invalid Command - `just demos::docker`
- **Line 102**: Invalid Command - `just demos::graphql`
- **Line 102**: Invalid Command - `just demos::migrations`
- **Line 7**: Invalid Command - `just demo-<feature>`
- **Line 18**: Invalid Command - `just demos::health`
- **Line 24**: Invalid Command - `just demos::api`
- **Line 31**: Invalid Command - `just demos::graphql`
- **Line 38**: Invalid Command - `just demos::docker`
- **Line 45**: Invalid Command - `just demos::migrations`
- **Line 51**: Invalid Command - `just demo-commits`
- **Line 57**: Invalid Command - `just demo-diff-generation`
- **Line 63**: Invalid Command - `just demos::all`
- **Line 73**: Invalid Command - `just demo-commits-docker`
- **Line 74**: Invalid Command - `just demo-diff-generation-docker`

### docs/development/https-setup.md

- **Line 99**: Invalid Path - `.env.https`
- **Line 118**: Invalid Path - `Proceed to haven.local`
- **Line 234**: Invalid Path - `myapp.local`
- **Line 235**: Invalid Path - `*.myapp.local`
- **Line 236**: Invalid Path - `api.myapp.local`
- **Line 247**: Invalid Path - `*.local`
- **Line 22**: Invalid Path - `//haven.local`
- **Line 23**: Invalid Path - `//api.haven.local`
- **Line 80**: Invalid Path - `/certs/key.pem`
- **Line 81**: Invalid Path - `/certs/cert.pem`
- **Line 92**: Invalid Path - `/etc/nginx`
- **Line 93**: Invalid Path - `/etc/nginx/certs`
- **Line 111**: Invalid Path - `//api.haven.local/api/v1`
- **Line 116**: Invalid Path - `Chrome/Edge`
- **Line 152**: Invalid Path - `//haven.local/auth/callback`
- **Line 221**: Invalid Path - `SSL/TLS`
- **Line 250**: Invalid Path - `/dev-certs/certs`

### docs/development/justfile-architecture.md

- **Line 97**: Invalid Path - `justfile.common`
- **Line 54**: Invalid Path - `js/TypeScript`
- **Line 120**: Invalid Path - `deployment/release`
- **Line 122**: Invalid Path - `CI/CD`

### docs/development/local-domains.md

- **Line 5**: Invalid Path - `web.haven.local`
- **Line 5**: Invalid Path - `api.haven.local`
- **Line 28**: Invalid Path - `haven.local`
- **Line 31**: Invalid Path - `app.haven.local`
- **Line 70**: Invalid Path - `/etc/hosts.haven.backup`
- **Line 17**: Invalid Path - `//haven.local`
- **Line 18**: Invalid Path - `//api.haven.local`
- **Line 19**: Invalid Path - `//api.haven.local/graphql`
- **Line 45**: Invalid Path - `//web.haven.local`
- **Line 167**: Invalid Path - `/operations/docker.md`

### docs/development/local-setup.md

- **Line 55**: Invalid Path - `docker-compose.yaml`
- **Line 117**: Invalid Path - `Implement pending tasks in todo.md`
- **Line 13**: Invalid Path - `//github.com/pyenv/pyenv`
- **Line 15**: Invalid Path - `//just.systems`
- **Line 23**: Invalid Path - `jazzydog-labs/haven.git`
- **Line 30**: Invalid Path - `//install.hatch.pm`
- **Line 35**: Invalid Path - `anthropic-ai/claude-code`
- **Line 48**: Invalid Path - `claude/settings.json`
- **Line 57**: Invalid Path - `local/pgdata`
- **Line 77**: Invalid Path - `//localhost`
- **Line 79**: Invalid Path - `8080/docs`
- **Line 80**: Invalid Path - `8080/graphql`
- **Line 102**: Invalid Path - `create/update`
- **Line 63**: Invalid Command - `just db-down         # stop and remove the compose stack`
- **Line 128**: Invalid Command - `just db-down     # stop containers`
- **Line 120**: Invalid Command - `just claude`
- **Line 77**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 79**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 80**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`

### docs/development/migration-strategies.md

- **Line 43**: Invalid Path - `CI/CD`
- **Line 27**: Invalid Command - `just database::migrate-docker`
- **Line 46**: Invalid Command - `just database::migrate-run`
- **Line 65**: Invalid Command - `just database::migrate-service`
- **Line 110**: Invalid Command - `just database::make "add_user_table"`
- **Line 110**: Invalid Command - `just database::make-docker "add_user_table"`
- **Line 124**: Invalid Command - `just database::history`
- **Line 124**: Invalid Command - `just database::history-docker`
- **Line 125**: Invalid Command - `just database::current`
- **Line 125**: Invalid Command - `just database::current-docker`
- **Line 126**: Invalid Command - `just database::downgrade`
- **Line 126**: Invalid Command - `just database::downgrade-docker`
- **Line 127**: Invalid Command - `just database::reset-docker`

### docs/development/quality.md

- **Line 155**: Invalid Path - `docs/definition-of-done.md`
- **Line 165**: Invalid Path - `pyrightconfig.json`
- **Line 40**: Invalid Path - `module/docstring`
- **Line 100**: Invalid Path - `//github.com/astral`
- **Line 100**: Invalid Path - `sh/ruff`
- **Line 106**: Invalid Path - `//github.com/microsoft/pyright`
- **Line 53**: Invalid Command - `just lint‑fix        # ruff check --fix . && ruff format .`
- **Line 151**: Invalid Command - `just docs`

### docs/development/refactoring.md

- **Line 39**: Invalid Path - `*.py`
- **Line 39**: Invalid Path - `s/src.old.path/src.new.path/g`
- **Line 45**: Invalid Path - `src/new/path`
- **Line 48**: Invalid Path - `src/old/path/`
- **Line 48**: Invalid Path - `src/new/path/`
- **Line 53**: Invalid Path - `github/workflows/`
- **Line 66**: Invalid Path - `src/services/everything.py`
- **Line 67**: Invalid Path - `src/services/`
- **Line 77**: Invalid Path - `src/api/utils.py`
- **Line 77**: Invalid Path - `src/common/`
- **Line 78**: Invalid Path - `src/graphql/utils.py`
- **Line 101**: Invalid Path - `conf/new_structure/`
- **Line 102**: Invalid Path - `conf/old_group`
- **Line 102**: Invalid Path - `conf/new_structure/group`
- **Line 108**: Invalid Path - `new_structure/group`
- **Line 121**: Invalid Path - `//...`
- **Line 124**: Invalid Path - `conf/database/postgres.yaml`
- **Line 167**: Invalid Path - `alembic/versions/xxx_add_new_column.py`
- **Line 173**: Invalid Path - `alembic/versions/yyy_copy_data.py`
- **Line 184**: Invalid Path - `alembic/versions/zzz_drop_old_column.py`
- **Line 204**: Invalid Path - `/api/v1/records`
- **Line 205**: Invalid Path - `/api/v2/records`
- **Line 26**: Invalid Command - `just grep "from src.old.path import"`

### docs/development/scalable-justfile.md

- **Line 364**: Invalid Path - `.just/discover-packages.sh`
- **Line 13**: Invalid Path - `recipes/variables`
- **Line 40**: Invalid Path - `just/common.just`
- **Line 45**: Invalid Path - `tools/deploy.just`
- **Line 48**: Invalid Path - `packages/api-gateway/justfile`
- **Line 49**: Invalid Path - `packages/auth-service/justfile`
- **Line 50**: Invalid Path - `packages/web-app/justfile`
- **Line 58**: Invalid Path - `just/help.sh`
- **Line 157**: Invalid Path - `y/N`
- **Line 188**: Invalid Path - `js/Express`
- **Line 189**: Invalid Path - `Python/FastAPI`
- **Line 190**: Invalid Path - `React/TypeScript`
- **Line 198**: Invalid Path - `just/completions.sh`
- **Line 364**: Invalid Path - `just/discover-packages.sh`
- **Line 377**: Invalid Path - `CI/CD`
- **Line 403**: Invalid Path - `templates/node-service`
- **Line 406**: Invalid Path - `templates/python-service`
- **Line 162**: Invalid Command - `just list-all          List all available commands`
- **Line 162**: Invalid Command - `just cd <path>         Show commands for specific directory`
- **Line 162**: Invalid Command - `just build             Build all packages`
- **Line 162**: Invalid Command - `just watch             Watch all services (opens tmux)`
- **Line 429**: Invalid Command - `just api::dev             # Start only API in dev mode`
- **Line 429**: Invalid Command - `just test-all             # Run all tests`
- **Line 429**: Invalid Command - `just test::integration    # Run integration tests`
- **Line 429**: Invalid Command - `just api::test-file user  # Test specific file`
- **Line 429**: Invalid Command - `just docker::up           # Start containers`
- **Line 429**: Invalid Command - `just docker::logs api     # Show API logs`
- **Line 429**: Invalid Command - `just docker::exec db psql # Access database`
- **Line 429**: Invalid Command - `just deploy::staging      # Deploy to staging`
- **Line 429**: Invalid Command - `just deploy::production   # Deploy to production`

### docs/development/tasks-workflow.md

- **Line 59**: Invalid Path - `docs/roadmap.md`
- **Line 62**: Invalid Path - `tasks/open/user-authentication.md`
- **Line 65**: Invalid Path - `docs/commits-plan.md`
- **Line 95**: Invalid Path - `graphql-subscriptions.md`
- **Line 96**: Invalid Path - `tasks/closed/basic-crud-operations.md`
- **Line 97**: Invalid Path - `work-log.md`
- **Line 97**: Invalid Path - `user-authentication.md`
- **Line 24**: Invalid Path - `tasks/open/graphql-pagination.md`
- **Line 25**: Invalid Path - `tasks/open/database-connection-pooling.md`
- **Line 70**: Invalid Path - `login/logout`
- **Line 86**: Invalid Path - `tasks/open/task-name.md`
- **Line 86**: Invalid Path - `tasks/closed/`
- **Line 110**: Invalid Path - `tasks/open/new-feature.md`
- **Line 116**: Invalid Path - `tasks/open/completed-task.md`

### docs/development/testing.md

- **Line 65**: Invalid Path - `@pytest.mark.parametrize`
- **Line 66**: Invalid Path - `monkeypatch.setattr`
- **Line 81**: Invalid Path - `tests/conftest.py`
- **Line 113**: Invalid Path - `tests/e2e/smoke_test.py`
- **Line 137**: Invalid Path - `@pytest.mark.slow`
- **Line 42**: Invalid Path - `src/haven/`
- **Line 50**: Invalid Path - `tests/unit`
- **Line 59**: Invalid Path - `print/debug`
- **Line 86**: Invalid Path - `conf/test`
- **Line 118**: Invalid Path - `//localhost`
- **Line 127**: Invalid Path - `tests/e2e`
- **Line 136**: Invalid Path - `setup/teardown.`
- **Line 143**: Invalid Path - `code/api`
- **Line 148**: Invalid Command - `just db-down`
- **Line 118**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`

### docs/development/ttr-demo.md

- **Line 66**: Invalid Path - `CI/CD`
- **Line 74**: Invalid Path - `tests/unit/domain/test_user.py`
- **Line 74**: Invalid Path - `tests/unit/domain/test_repository.py`
- **Line 77**: Invalid Path - `tests/unit/application/test_user_service.py`
- **Line 77**: Invalid Path - `tests/unit/application/test_repository_service.py`
- **Line 80**: Invalid Path - `tests/unit/infrastructure/test_user_repository.py`
- **Line 80**: Invalid Path - `tests/unit/infrastructure/test_repository_repository.py`
- **Line 146**: Invalid Path - `jazzydog-labs/haven`
- **Line 156**: Invalid Path - `user/test-repo`
- **Line 157**: Invalid Path - `//github.com/user/test-repo.git`
- **Line 7**: Invalid Command - `just demos::ttr`
- **Line 231**: Invalid Command - `just database::current`
- **Line 231**: Invalid Command - `just database::history`
- **Line 243**: Invalid Command - `just testing::coverage`

### docs/index.md

- **Line 19**: Invalid Path - `Async/await`
- **Line 30**: Invalid Path - `OpenAPI/Swagger`
- **Line 59**: Invalid Path - `//jazzydog-labs.github.io/haven`
- **Line 60**: Invalid Path - `//github.com/jazzydog-labs/haven/issues`
- **Line 61**: Invalid Path - `//github.com/jazzydog-labs/haven/discussions`
- **Line 49**: Broken Link - [Architecture Overview](architecture.md)
- **Line 51**: Broken Link - [Development Guide](local-setup.md)
- **Line 55**: Broken Link - [Roadmap](roadmap.md)

### docs/operations/cli.md

- **Line 63**: Invalid Path - `index.html`
- **Line 117**: Invalid Path - `01-abc12345-commit-message.html`
- **Line 83**: Invalid Path - `diff-output/index.html`
- **Line 153**: Invalid Path - `api/diff-generation.md`
- **Line 101**: Invalid Command - `just cli-list-commits                    # List commits`
- **Line 101**: Invalid Command - `just cli-generate                       # Generate diffs`
- **Line 101**: Invalid Command - `just cli-generate-to /path/to/output    # Generate to specific directory`
- **Line 101**: Invalid Command - `just demo-commits           # Full demo with auto-server startup`
- **Line 101**: Invalid Command - `just demo-diff-generation   # Uses API server (requires manual startup)`
- **Line 153**: Broken Link - [API Documentation](api/diff-generation.md)
- **Line 155**: Broken Link - [Architecture](architecture.md)

### docs/operations/container-troubleshooting.md

- **Line 39**: Invalid Path - `macOS/Linux`
- **Line 101**: Invalid Path - `//haven`
- **Line 101**: Invalid Path - `5432/haven`
- **Line 136**: Invalid Path - `/app/src`
- **Line 148**: Invalid Path - `/apps/api`
- **Line 158**: Invalid Path - `/apps/api/src`
- **Line 164**: Invalid Path - `/Users/name/project`
- **Line 231**: Invalid Path - `//localhost`
- **Line 231**: Invalid Path - `8080/health`
- **Line 241**: Invalid Path - `//api`
- **Line 231**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`

### docs/operations/deployment.md

- **Line 284**: Invalid Path - `haven_*.sql.gz`
- **Line 18**: Invalid Path - `com/haven`
- **Line 46**: Invalid Path - `/var/lib/postgresql/data`
- **Line 68**: Invalid Path - `apps/v1`
- **Line 120**: Invalid Path - `//user`
- **Line 120**: Invalid Path - `5432/dbname`
- **Line 160**: Invalid Path - `/health/ready`
- **Line 161**: Invalid Path - `/health/live`
- **Line 192**: Invalid Path - `//jaeger`
- **Line 199**: Invalid Path - `HTTPS/TLS`
- **Line 208**: Invalid Path - `/etc/ssl/certs/cert.pem`
- **Line 209**: Invalid Path - `/etc/ssl/private/key.pem`
- **Line 212**: Invalid Path - `//haven`
- **Line 280**: Invalid Path - `BACKUP_DIR/haven_`
- **Line 303**: Invalid Path - `deployment/haven`
- **Line 322**: Invalid Path - `I/O`
- **Line 340**: Broken Link - [Configuration Reference](configuration.md)

### docs/operations/docker-quick-reference.md

- **Line 81**: Invalid Path - `/app/.tmp`
- **Line 76**: Invalid Path - `/apps/api/src`
- **Line 76**: Invalid Path - `/app/src`
- **Line 77**: Invalid Path - `/apps/api/conf`
- **Line 77**: Invalid Path - `/app/conf`
- **Line 78**: Invalid Path - `/apps/api/alembic`
- **Line 78**: Invalid Path - `/app/alembic`
- **Line 79**: Invalid Path - `/apps/api/logs`
- **Line 79**: Invalid Path - `/app/logs`
- **Line 80**: Invalid Path - `/apps/api/tests`
- **Line 80**: Invalid Path - `/app/tests`
- **Line 86**: Invalid Path - `//localhost`
- **Line 87**: Invalid Path - `8080/health`
- **Line 88**: Invalid Path - `8080/docs`
- **Line 89**: Invalid Path - `8080/graphql`
- **Line 5**: Invalid Command - `just docker::reset             # Full reset (removes data)`
- **Line 5**: Invalid Command - `just docker::shell             # Shell into API container`
- **Line 5**: Invalid Command - `just database::console-docker        # PostgreSQL console`
- **Line 5**: Invalid Command - `just docker::test              # Run tests in container`
- **Line 5**: Invalid Command - `just docker::lint              # Run linting in container`
- **Line 5**: Invalid Command - `just clean-docker                             # Project cleanup`
- **Line 86**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 87**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 88**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 89**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`

### docs/operations/docker.md

- **Line 84**: Invalid Path - `compose.yaml`
- **Line 14**: Invalid Path - `dev/chainguard/python`
- **Line 14**: Invalid Path - `linux/arm64`
- **Line 14**: Invalid Path - `linux/amd64`
- **Line 27**: Invalid Path - `/root/.cache`
- **Line 34**: Invalid Path - `/tmp/req.txt`
- **Line 34**: Invalid Path - `/usr/local/lib/python3.12/site-packages`
- **Line 37**: Invalid Path - `/app/src`
- **Line 42**: Invalid Path - `//github.com/jazzydog-labs/haven`
- **Line 53**: Invalid Path - `/app/out/`
- **Line 60**: Invalid Path - `/sbin/tini`
- **Line 96**: Invalid Path - `//security.scw.cloud`
- **Line 100**: Invalid Path - `//github.com/chainguard-images`

### docs/operations/monitoring.md

- **Line 46**: Invalid Path - `haven.api`
- **Line 175**: Invalid Path - `record.id`
- **Line 180**: Invalid Path - `result.status`
- **Line 51**: Invalid Path - `/api/v1/records`
- **Line 117**: Invalid Path - `//localhost`
- **Line 117**: Invalid Path - `8080/metrics`
- **Line 137**: Invalid Path - `I/O`
- **Line 156**: Invalid Path - `//jaeger`
- **Line 189**: Invalid Path - `/health/live`
- **Line 194**: Invalid Path - `/health/ready`
- **Line 320**: Invalid Path - `8080/admin/debug`
- **Line 388**: Invalid Path - `created/updated`
- **Line 431**: Broken Link - [Configuration Reference](configuration.md)
- **Line 432**: Broken Link - [Troubleshooting Guide](troubleshooting.md)
- **Line 117**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 320**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`

### docs/overview.md

- **Line 186**: Invalid Path - `docs/architecture.md`
- **Line 188**: Invalid Path - `docs/alembic.md`
- **Line 189**: Invalid Path - `docs/definition-of-done.md`
- **Line 192**: Invalid Path - `docs/local-setup.md`
- **Line 193**: Invalid Path - `docs/testing.md`
- **Line 194**: Invalid Path - `docs/quality.md`
- **Line 195**: Invalid Path - `docs/configuration.md`
- **Line 198**: Invalid Path - `docs/refactoring.md`
- **Line 199**: Invalid Path - `work-log.md`
- **Line 200**: Invalid Path - `docs/roadmap.md`
- **Line 201**: Invalid Path - `todo.md`
- **Line 204**: Invalid Path - `docs/spec.md`
- **Line 207**: Invalid Path - `docs/commits-plan.md`
- **Line 105**: Invalid Path - `CI/CD`
- **Line 120**: Invalid Path - `Request/response`
- **Line 245**: Invalid Path - `TypeScript/React`
- **Line 265**: Invalid Path - `/scripts/demo-commits.sh`
- **Line 265**: Invalid Path - `venv/bin/python`
- **Line 233**: Invalid Command - `just type-python       # Python type checking`
- **Line 233**: Invalid Command - `just check-python      # All Python quality gates`
- **Line 233**: Invalid Command - `just check-web         # All TypeScript quality gates`
- **Line 233**: Invalid Command - `just docs              # Build documentation`
- **Line 233**: Invalid Command - `just demo-commits      # Demo git diff viewer (auto-starts server)`
- **Line 233**: Invalid Command - `just demo-diff-generation  # Demo git diff API (requires server)`
- **Line 233**: Invalid Command - `just --list            # Show all available commands`
- **Line 233**: Invalid Command - `just cli-list-commits          # List commits via Just command`
- **Line 233**: Invalid Command - `just cli-generate             # Generate HTML diffs via Just command`
- **Line 233**: Invalid Command - `just cli-generate-to /path    # Generate diffs to specific directory`
- **Line 186**: Broken Link - [`docs/architecture.md`](architecture.md)
- **Line 188**: Broken Link - [`docs/alembic.md`](alembic.md)
- **Line 189**: Broken Link - [`docs/definition-of-done.md`](definition-of-done.md)
- **Line 192**: Broken Link - [`docs/local-setup.md`](local-setup.md)
- **Line 193**: Broken Link - [`docs/testing.md`](testing.md)
- **Line 194**: Broken Link - [`docs/quality.md`](quality.md)
- **Line 195**: Broken Link - [`docs/configuration.md`](configuration.md)
- **Line 198**: Broken Link - [`docs/refactoring.md`](refactoring.md)
- **Line 199**: Broken Link - [`work-log.md`](../work-log.md)
- **Line 200**: Broken Link - [`docs/roadmap.md`](roadmap.md)
- **Line 201**: Broken Link - [`todo.md`](../todo.md)
- **Line 204**: Broken Link - [`docs/spec.md`](spec.md)
- **Line 205**: Broken Link - [`docs/architecture.md`](architecture.md)
- **Line 207**: Broken Link - [`docs/commits-plan.md`](commits-plan.md)

### docs/project-management/ai-conversations/claude-solo.md

- **Line 19**: Invalid Path - `mkdir -p .claude`
- **Line 98**: Invalid Path - `guardrails/checklist.yaml`
- **Line 65**: Invalid Path - `Create the Stop and PreToolUse hooks described in SPEC.md`
- **Line 9**: Invalid Path - `anthropic-ai/claude-code`
- **Line 20**: Invalid Path - `claude/settings.json`
- **Line 151**: Invalid Path - `//docs.anthropic.com/en/docs/claude-code/setup`
- **Line 152**: Invalid Path - `//docs.anthropic.com/en/docs/claude-code/iam`
- **Line 153**: Invalid Path - `//docs.anthropic.com/en/docs/claude-code/security`
- **Line 154**: Invalid Path - `//docs.anthropic.com/en/docs/claude-code/hooks`
- **Line 155**: Invalid Path - `//docs.anthropic.com/en/docs/claude-code/cli-reference`
- **Line 156**: Invalid Path - `//docs.anthropic.com/en/docs/claude-code/quickstart`
- **Line 157**: Invalid Path - `//docs.anthropic.com/en/docs/claude-code/interactive-mode`
- **Line 114**: Invalid Command - `just implement`
- **Line 92**: Invalid Command - `just plan "Add Tag entity"`
- **Line 92**: Invalid Command - `just implement`

### docs/project-management/commits-plan.md

- **Line 20**: Invalid Path - `Python/TypeScript`
- **Line 29**: Invalid Path - `requests/responses`
- **Line 30**: Invalid Path - `schema/resolvers`
- **Line 31**: Invalid Path - `queries/mutations`
- **Line 110**: Invalid Path - `async/await`

### docs/project-management/roadmap.md

- **Line 59**: Invalid Path - `CI/CD`
- **Line 60**: Invalid Path - `Prometheus/Grafana`
- **Line 75**: Invalid Path - `REST/GraphQL`
- **Line 76**: Invalid Path - `OpenAPI/GraphQL`
- **Line 176**: Invalid Path - `feature/fix`
- **Line 179**: Invalid Path - `roadmap/todo`

### docs/project-management/spec.md

- **Line 65**: Invalid Path - `conf/{environment}/{component}.yaml`
- **Line 35**: Invalid Path - `I/O`
- **Line 66**: Invalid Path - `conf/local`
- **Line 76**: Invalid Path - `query/mutation`
- **Line 97**: Invalid Path - `up/down`
- **Line 133**: Invalid Path - `docs/adr/`
- **Line 149**: Invalid Path - `Authentication/authorization`
- **Line 152**: Invalid Path - `CI/CD`
- **Line 24**: Invalid Command - `just docs`
- **Line 96**: Invalid Command - `just install`
- **Line 101**: Invalid Command - `just docs`
- **Line 102**: Invalid Command - `just build`
- **Line 132**: Invalid Command - `just docs`
- **Line 139**: Invalid Command - `just install && just database::up && just run`

### docs/project-management/tasks/closed/container-dev-experience.md

- **Line 7**: Invalid Path - `macOS/Linux`

### docs/project-management/tasks/closed/container-troubleshooting-guide.md

- **Line 47**: Invalid Path - `Proxy/firewall`
- **Line 65**: Invalid Path - `macOS/Linux`
- **Line 78**: Invalid Path - `macOS/Linux/Windows`
- **Line 80**: Invalid Path - `docs/docker.md`

### docs/project-management/tasks/closed/containerize-api-service.md

- **Line 30**: Invalid Path - `/apps/api/src`
- **Line 30**: Invalid Path - `/app/src`
- **Line 31**: Invalid Path - `/apps/api/conf`
- **Line 31**: Invalid Path - `/app/conf`
- **Line 35**: Invalid Path - `//haven`
- **Line 35**: Invalid Path - `5432/haven`
- **Line 42**: Invalid Path - `//localhost`
- **Line 42**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`

### docs/project-management/tasks/closed/containerize-services.md

- **Line 13**: Invalid Path - `start/stop`

### docs/project-management/tasks/closed/create-dev-overrides.md

- **Line 25**: Invalid Path - `/apps/api/src`
- **Line 25**: Invalid Path - `/app/src`
- **Line 26**: Invalid Path - `/apps/api/conf`
- **Line 26**: Invalid Path - `/app/conf`
- **Line 27**: Invalid Path - `/apps/api/alembic`
- **Line 27**: Invalid Path - `/app/alembic`
- **Line 28**: Invalid Path - `/apps/api/.venv`
- **Line 28**: Invalid Path - `/app/.venv`

### docs/project-management/tasks/closed/crud-frontend-records.md

- **Line 12**: Invalid Path - `Search/filter`
- **Line 24**: Invalid Path - `Create/Edit`
- **Line 25**: Invalid Path - `modal/page`
- **Line 44**: Invalid Path - `types/record.ts`
- **Line 59**: Invalid Path - `services/api/records.ts`
- **Line 62**: Invalid Path - `/api/v1/records`
- **Line 71**: Invalid Path - `/api/v1/records/`
- **Line 95**: Invalid Path - `created/updated`

### docs/project-management/tasks/closed/frontend-backend-sync-workflow.md

- **Line 8**: Invalid Path - `OpenAPI/Swagger`
- **Line 11**: Invalid Path - `CI/CD`
- **Line 18**: Invalid Path - `//localhost`
- **Line 18**: Invalid Path - `8080/openapi.json`
- **Line 23**: Invalid Path - `apps/web/src/types/domain.ts`
- **Line 33**: Invalid Path - `apps/web/src/services/api/generated`
- **Line 44**: Invalid Path - `8080/health`
- **Line 75**: Invalid Path - `github/workflows/api-compatibility.yml`
- **Line 88**: Invalid Path - `actions/checkout`
- **Line 91**: Invalid Path - `oasdiff/oasdiff-action`
- **Line 93**: Invalid Path - `origin/main`
- **Line 105**: Invalid Path - `/scripts/sync-frontend-backend.sh`
- **Line 110**: Invalid Path - `apps/api/openapi.json`
- **Line 116**: Invalid Path - `/scripts/generate-crud.sh`
- **Line 121**: Invalid Path - `githooks/pre-commit`
- **Line 124**: Invalid Path - `domain/entities`
- **Line 129**: Invalid Path - `interface/api`
- **Line 139**: Invalid Path - `Add/modify`
- **Line 18**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 31**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 44**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 51**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 57**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 109**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`

### docs/project-management/tasks/closed/implement-migration-strategy.md

- **Line 42**: Invalid Path - `//haven`
- **Line 42**: Invalid Path - `5432/haven`
- **Line 51**: Invalid Path - `dev/staging/prod`
- **Line 52**: Invalid Path - `CI/CD`
- **Line 58**: Invalid Path - `pros/cons`

### docs/project-management/tasks/closed/local-cors-and-domains.md

- **Line 54**: Invalid Path - `haven.local`
- **Line 21**: Invalid Path - `//localhost`
- **Line 23**: Invalid Path - `//app.haven.local`
- **Line 21**: Localhost Url - `http://web.haven.local` → `http://web.haven.local`
- **Line 22**: Localhost Url - `http://localhost:5173` → `http://haven.local:5173`

### docs/project-management/tasks/closed/local-https-setup.md

- **Line 25**: Invalid Path - `Docker/FastAPI`
- **Line 39**: Invalid Path - `/etc/caddy/Caddyfile`
- **Line 59**: Invalid Path - `/etc/nginx/certs/cert.pem`
- **Line 60**: Invalid Path - `/etc/nginx/certs/key.pem`
- **Line 63**: Invalid Path - `//api`
- **Line 73**: Invalid Path - `cameronhunter/local-ssl-proxy`
- **Line 91**: Invalid Path - `//api.haven.local`
- **Line 92**: Invalid Path - `//api.production.com`

### docs/project-management/tasks/closed/modular-justfiles.md

- **Line 4**: Invalid Path - `build/test/deployment`
- **Line 7**: Invalid Path - `Python/TypeScript`
- **Line 10**: Invalid Path - `import/inclusion`
- **Line 19**: Invalid Path - `api/justfile`
- **Line 20**: Invalid Path - `client/justfile`
- **Line 20**: Invalid Path - `React/TypeScript`
- **Line 28**: Invalid Path - `TypeScript/React`
- **Line 42**: Invalid Path - `CI/CD`
- **Line 29**: Invalid Command - `just demo-*`
- **Line 40**: Invalid Command - `just api:test`

### docs/project-management/tasks/closed/reorganize-project-structure.md

- **Line 13**: Invalid Path - `CI/CD`
- **Line 21**: Invalid Path - `Example/demo`

### docs/project-management/tasks/closed/ttr-comment-domain-entity.md

- **Line 15**: Invalid Path - `src/haven/domain/entities/comment.py`
- **Line 67**: Invalid Path - `src/haven/infrastructure/database/models/comment.py`
- **Line 99**: Invalid Path - `src/haven/application/services/comment_service.py`
- **Line 156**: Invalid Path - `src/haven/domain/repositories/comment_repository.py`
- **Line 206**: Invalid Path - `tests/unit/domain/entities/test_comment.py`
- **Line 273**: Invalid Path - `tests/unit/application/services/test_comment_service.py`
- **Line 79**: Invalid Path - `commits.id`
- **Line 80**: Invalid Path - `users.id`
- **Line 232**: Invalid Path - `src/main.py`
- **Line 201**: Invalid Command - `just database::make "create_comments_table"`

### docs/project-management/tasks/closed/ttr-repository-domain-entity.md

- **Line 15**: Invalid Path - `src/haven/domain/entities/repository.py`
- **Line 60**: Invalid Path - `src/haven/infrastructure/database/models/repository.py`
- **Line 86**: Invalid Path - `src/haven/application/services/repository_service.py`
- **Line 119**: Invalid Path - `tests/unit/domain/entities/test_repository.py`
- **Line 56**: Invalid Path - `github.com`
- **Line 128**: Invalid Path - `jazzydog-labs/haven`
- **Line 157**: Invalid Path - `user/test`
- **Line 158**: Invalid Path - `//github.com/user/test.git`
- **Line 114**: Invalid Command - `just database::make "create_repositories_table"`

### docs/project-management/tasks/closed/ttr-user-domain-entity.md

- **Line 15**: Invalid Path - `src/haven/domain/entities/user.py`
- **Line 49**: Invalid Path - `src/haven/infrastructure/database/models/user.py`
- **Line 81**: Invalid Path - `tests/unit/domain/entities/test_user.py`
- **Line 9**: Invalid Path - `dataclass/model`
- **Line 76**: Invalid Command - `just database::make "create_users_table"`

### docs/project-management/tasks/closed/update-containerization-docs.md

- **Line 31**: Invalid Path - `//localhost`
- **Line 32**: Invalid Path - `8080/graphql`
- **Line 44**: Invalid Path - `migrations/models`
- **Line 65**: Invalid Path - `CI/CD`
- **Line 87**: Invalid Path - `8080/5432`
- **Line 19**: Invalid Command - `just run-api-docker         # Start API with hot-reload`
- **Line 19**: Invalid Command - `just database::migrate-docker`
- **Line 60**: Invalid Command - `just database::make "add_user_table"    # Generate migration`
- **Line 66**: Invalid Command - `just database::migrate-docker           # Apply migrations`
- **Line 66**: Invalid Command - `just database::make-docker "add_field"  # Generate in container`
- **Line 31**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 32**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`

### docs/project-management/tasks/closed/worklog-demo-commands.md

- **Line 4**: Invalid Path - `work-log.md`
- **Line 17**: Invalid Path - `output/feedback`
- **Line 32**: Invalid Path - `success/failure`
- **Line 4**: Invalid Command - `just demo-*`
- **Line 8**: Invalid Command - `just demo-*`
- **Line 15**: Invalid Command - `just demo-<feature-name>`
- **Line 18**: Invalid Command - `just demos::all`
- **Line 22**: Invalid Command - `just demo-diffs`
- **Line 23**: Invalid Command - `just demos::graphql`
- **Line 24**: Invalid Command - `just demos::api`
- **Line 25**: Invalid Command - `just demos::health`

### docs/project-management/tasks/open/production-like-local-env.md

- **Line 51**: Invalid Path - `haven.local`
- **Line 73**: Invalid Path - `127.0.0.1 haven.local`
- **Line 17**: Invalid Path - `//haven.local`
- **Line 46**: Invalid Path - `/etc/traefik/traefik.yml`
- **Line 99**: Invalid Path - `//haven.local/api`
- **Line 123**: Invalid Path - `Traefik/Caddy`

### docs/project-management/tasks/open/ttr-commit-domain-entity.md

- **Line 15**: Invalid Path - `src/haven/domain/entities/commit.py`
- **Line 104**: Invalid Path - `src/haven/infrastructure/database/models/commit.py`
- **Line 162**: Invalid Path - `src/haven/application/services/commit_service.py`
- **Line 227**: Invalid Path - `tests/unit/domain/entities/test_commit.py`
- **Line 117**: Invalid Path - `repositories.id`
- **Line 148**: Invalid Path - `commits.id`
- **Line 149**: Invalid Path - `users.id`
- **Line 222**: Invalid Command - `just database::make "create_commits_and_reviews_tables"`

### docs/project-management/todo.md

- **Line 45**: Invalid Path - `tasks/open/frontend-backend-sync-workflow.md`
- **Line 50**: Invalid Path - `implement-scalable-justfile-system.md`
- **Line 53**: Invalid Path - `comprehensive-docs-audit.md`
- **Line 56**: Invalid Path - `crud-frontend-records.md`
- **Line 57**: Invalid Path - `frontend-backend-sync-workflow.md`
- **Line 60**: Invalid Path - `local-https-setup.md`
- **Line 61**: Invalid Path - `production-like-local-env.md`
- **Line 71**: Invalid Path - `docs/roadmap.md`
- **Line 72**: Invalid Path - `docs/commits-plan.md`
- **Line 73**: Invalid Path - `docs/architecture.md`
- **Line 77**: Invalid Path - `docs/definition-of-done.md`

### docs/project-management/work-log.md

- **Line 112**: Invalid Path - `src/haven/domain/entities/repository.py`
- **Line 112**: Invalid Path - `src/haven/infrastructure/database/repositories/repository_repository.py`
- **Line 113**: Invalid Path - `just test tests/unit/domain/test_repository.py tests/unit/infrastructure/test_repository_repository.py tests/unit/application/test_repository_service.py`
- **Line 140**: Invalid Path - `src/haven/domain/entities/user.py`
- **Line 140**: Invalid Path - `src/haven/infrastructure/database/repositories/user_repository.py`
- **Line 141**: Invalid Path - `just test tests/unit/domain/test_user.py tests/unit/infrastructure/test_user_repository.py tests/unit/application/test_user_service.py`
- **Line 417**: Invalid Path - `justfile.demos`
- **Line 445**: Invalid Path - `sudo ./scripts/setup-local-domains.sh`
- **Line 10**: Invalid Path - `venv/bin/python`
- **Line 17**: Invalid Path - `//localhost`
- **Line 17**: Invalid Path - `8080/api/v1/ttr/tasks`
- **Line 18**: Invalid Path - `8080/docs`
- **Line 21**: Invalid Path - `8080/graphql`
- **Line 44**: Invalid Path - `tasks/milestones`
- **Line 113**: Invalid Path - `tests/unit/domain/test_repository.py`
- **Line 113**: Invalid Path - `tests/unit/infrastructure/test_repository_repository.py`
- **Line 113**: Invalid Path - `tests/unit/application/test_repository_service.py`
- **Line 117**: Invalid Path - `venv/bin/activate`
- **Line 141**: Invalid Path - `tests/unit/domain/test_user.py`
- **Line 141**: Invalid Path - `tests/unit/infrastructure/test_user_repository.py`
- **Line 141**: Invalid Path - `tests/unit/application/test_user_service.py`
- **Line 205**: Invalid Path - `docs/roadmap.md`
- **Line 218**: Invalid Path - `8080/api/v1/diffs/generate`
- **Line 218**: Invalid Path - `application/json`
- **Line 227**: Invalid Path - `8080/api/v1/diffs/status/`
- **Line 230**: Invalid Path - `tmp/diff-output/diff-out-`
- **Line 281**: Invalid Path - `apps/api/htmlcov/index.html`
- **Line 299**: Invalid Path - `tmp/diff-output/`
- **Line 342**: Invalid Path - `CI/CD`
- **Line 357**: Invalid Path - `pros/cons`
- **Line 382**: Invalid Path - `macOS/Windows/Linux`
- **Line 383**: Invalid Path - `printing/bookmarking`
- **Line 445**: Invalid Path - `/scripts/setup-local-domains.sh`
- **Line 458**: Invalid Path - `//api.haven.local`
- **Line 458**: Invalid Path - `8080/health`
- **Line 459**: Invalid Path - `//app.haven.local`
- **Line 462**: Invalid Path - `//haven.local/api/v1/records`
- **Line 463**: Invalid Path - `//haven.local/health`
- **Line 501**: Invalid Path - `Create/edit`
- **Line 502**: Invalid Path - `loading/error`
- **Line 576**: Invalid Path - `//haven.local`
- **Line 614**: Invalid Path - `//web.haven.local`
- **Line 616**: Invalid Path - `//api.haven.local/docs`
- **Line 627**: Invalid Path - `add/remove`
- **Line 636**: Invalid Path - `just/help.sh`
- **Line 661**: Invalid Path - `just/common.just`
- **Line 170**: Invalid Command - `just check-python # Python lint + type + test (was missing)`
- **Line 170**: Invalid Command - `just check-web   # Web lint + type + test (was missing)`
- **Line 245**: Invalid Command - `just demos::docker`
- **Line 245**: Invalid Command - `just demos::health`
- **Line 245**: Invalid Command - `just docker::test`
- **Line 245**: Invalid Command - `just database::console-docker`
- **Line 276**: Invalid Command - `just testing::coverage`
- **Line 276**: Invalid Command - `just demos::api`
- **Line 276**: Invalid Command - `just demos::graphql`
- **Line 334**: Invalid Command - `just demos::migrations`
- **Line 334**: Invalid Command - `just database::current-docker`
- **Line 334**: Invalid Command - `just database::migrate-run`
- **Line 334**: Invalid Command - `just --list | grep db-.*-docker`
- **Line 364**: Invalid Command - `just docker::reset`
- **Line 420**: Invalid Command - `just demos::health      # Health endpoints`
- **Line 420**: Invalid Command - `just demos::api         # REST CRUD operations`
- **Line 420**: Invalid Command - `just demos::graphql     # GraphQL queries`
- **Line 420**: Invalid Command - `just demos::docker      # Container status`
- **Line 420**: Invalid Command - `just demos::migrations  # Migration strategies`
- **Line 420**: Invalid Command - `just demos::all`
- **Line 447**: Invalid Command - `just demos::cors`
- **Line 518**: Invalid Command - `just demos::sync`
- **Line 526**: Invalid Command - `just check-api-compat`
- **Line 556**: Invalid Command - `just demos::https`
- **Line 638**: Invalid Command - `just --list         # All commands`
- **Line 638**: Invalid Command - `just docker::help   # Module help`
- **Line 638**: Invalid Command - `just testing::all   # Module commands`
- **Line 646**: Invalid Command - `just database::up        # Start PostgreSQL`
- **Line 646**: Invalid Command - `just docker::logs api    # View API logs`
- **Line 646**: Invalid Command - `just testing::python     # Run Python tests`
- **Line 646**: Invalid Command - `just demos::all          # Run all demos`
- **Line 10**: Invalid Command - `just docker::test`
- **Line 168**: Invalid Command - `just --list`
- **Line 243**: Invalid Command - `just docker::test`
- **Line 269**: Invalid Command - `just database::migrate-docker`
- **Line 299**: Invalid Command - `just demo-diff-generation`
- **Line 300**: Invalid Command - `just demo-diff-generation`
- **Line 332**: Invalid Command - `just database::current-docker`
- **Line 332**: Invalid Command - `just database::migrate-run`
- **Line 390**: Invalid Command - `just --list`
- **Line 418**: Invalid Command - `just demos::all`
- **Line 445**: Invalid Command - `just demos::cors`
- **Line 17**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 18**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 21**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 218**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 222**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 227**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 494**: Localhost Url - `http://web.haven.local` → `http://web.haven.local`

### docs/quickstart.md

- **Line 9**: Invalid Path - `//github.com/casey/just`
- **Line 16**: Invalid Path - `//github.com/jazzydog-labs/haven.git`
- **Line 43**: Invalid Path - `venv/bin/activate`
- **Line 60**: Invalid Path - `//localhost`
- **Line 64**: Invalid Path - `8080/health`
- **Line 71**: Invalid Path - `8080/docs`
- **Line 75**: Invalid Path - `8080/graphql`
- **Line 83**: Invalid Path - `8080/api/v1/records`
- **Line 84**: Invalid Path - `application/json`
- **Line 141**: Invalid Path - `8080/api/v1/records/`
- **Line 206**: Invalid Path - `//github.com/jazzydog-labs/haven/issues`
- **Line 161**: Invalid Command - `just --list`
- **Line 177**: Broken Link - [Architecture Overview](architecture.md)
- **Line 179**: Broken Link - [Development Environment](local-setup.md)
- **Line 180**: Broken Link - [Testing](testing.md)
- **Line 180**: Broken Link - [Code Quality](quality.md)
- **Line 60**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 64**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 71**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 71**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 75**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 75**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 83**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 120**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`
- **Line 141**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`

### docs/workflow/frontend-backend-sync.md

- **Line 62**: Invalid Path - `apps/web/src/types/openapi.prev.json`
- **Line 15**: Invalid Path - `request/response`
- **Line 81**: Invalid Path - `githooks/pre-commit`
- **Line 82**: Invalid Path - `domain/entities`
- **Line 87**: Invalid Path - `CI/CD`
- **Line 139**: Invalid Path - `hey-api/openapi-ts`
- **Line 140**: Invalid Path - `//localhost`
- **Line 140**: Invalid Path - `8080/openapi.json`
- **Line 141**: Invalid Path - `apps/web/src/services/api/generated`
- **Line 19**: Invalid Command - `just check-api-compat`
- **Line 140**: Localhost Url - `http://api.haven.local` → `http://api.haven.local`

### docs/workflow/normalize-docs.md

- **Line 52**: Invalid Path - `consistency-report.md`
- **Line 250**: Invalid Path - `scripts/generate-consistency-report.py`
- **Line 251**: Invalid Path - `tests/test_documentation.py`
- **Line 252**: Invalid Path - `requirements-docs.txt`
- **Line 255**: Invalid Path - `scripts/fix-common-issues.py`
- **Line 257**: Invalid Path - `scripts/check-external-links.py`
- **Line 110**: Invalid Path - `request/response`
- **Line 183**: Invalid Path - `fix/critical-docs-issues`
- **Line 188**: Invalid Path - `fix/important-docs-updates`
- **Line 193**: Invalid Path - `fix/minor-docs-cleanup`
- **Line 239**: Invalid Path - `CI/CD`
- **Line 240**: Invalid Path - `github/workflows/docs-check.yml`
- **Line 243**: Invalid Path - `weekly/monthly`
- **Line 279**: Invalid Path - `compile/run`
- **Line 293**: Invalid Path - `movements/renames`
- **Line 59**: Invalid Command - `just docker::test`
