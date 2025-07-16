# Documentation Audit Report

## Summary

- **Files Scanned**: 73
- **Files with Issues**: 67
- **Total Issues**: 1650

### Issues by Type

- **Invalid Paths**: 1144
- **Invalid Commands**: 435
- **Broken Links**: 65
- **Localhost Urls**: 6

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
- **Line 23**: Invalid Command - `just docker::up-d`
- **Line 37**: Invalid Command - `just database::up     # Start PostgreSQL`
- **Line 37**: Invalid Command - `just testing::fast    # Run unit tests only (quick feedback)`
- **Line 62**: Invalid Command - `just api::add-entity User`
- **Line 62**: Invalid Command - `just database::make "add_users_table" && just database::migrate`
- **Line 142**: Invalid Command - `just database::make "add_status_to_items"`
- **Line 142**: Invalid Command - `just database::migrate`
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
- **Line 41**: Invalid Path - `//api.haven.local/docs`
- **Line 42**: Invalid Path - `//api.haven.local/graphql`
- **Line 43**: Invalid Path - `//api.haven.local/health`
- **Line 49**: Invalid Path - `src/haven/`
- **Line 67**: Invalid Path - `//github.com/casey/just`
- **Line 86**: Invalid Path - `tests/unit/domain/test_record.py`
- **Line 111**: Invalid Path - `//api.haven.local/api/v1/records`
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
- **Line 22**: Invalid Command - `just database::up`
- **Line 22**: Invalid Command - `just database::migrate`
- **Line 71**: Invalid Command - `just --list      # Show all available commands`
- **Line 71**: Invalid Command - `just docs-serve  # Preview documentation locally`
- **Line 71**: Invalid Command - `just docker-build # Build Docker image`
- **Line 81**: Invalid Command - `just test-file tests/unit/domain/test_record.py`
- **Line 81**: Invalid Command - `just testing::coverage`
- **Line 147**: Broken Link - [Architecture Overview](docs/architecture.md)
- **Line 148**: Broken Link - [Local Setup Guide](docs/local-setup.md)
- **Line 150**: Broken Link - [Testing Guide](docs/testing.md)
- **Line 151**: Broken Link - [Deployment Guide](docs/deployment.md)

### apps/api/README.md

- **Line 9**: Invalid Path - `async/await`
- **Line 25**: Invalid Path - `//api.haven.local/docs`
- **Line 26**: Invalid Path - `//api.haven.local/graphql`
- **Line 27**: Invalid Path - `//api.haven.local/health`
- **Line 61**: Invalid Path - `//api.haven.local/api/v1/records`
- **Line 62**: Invalid Path - `application/json`
- **Line 16**: Invalid Command - `just database::up`
- **Line 16**: Invalid Command - `just database::migrate`
- **Line 48**: Invalid Command - `just testing::python      # Run test suite`
- **Line 48**: Invalid Command - `just type-python      # Type checking`
- **Line 48**: Invalid Command - `just format-python    # Format code`

### apps/web/README.md

- **Line 25**: Invalid Path - `//web.haven.local`
- **Line 25**: Invalid Path - `//api.haven.local.`
- **Line 61**: Invalid Path - `//api.haven.local/api/`
- **Line 62**: Invalid Path - `//api.haven.local/graphql`

### docs/api/diff-generation.md

- **Line 95**: Invalid Path - `scripts/demo-diff-generation.py`
- **Line 29**: Invalid Path - `//api.haven.local/api/v1/diffs/generate`
- **Line 30**: Invalid Path - `application/json`
- **Line 42**: Invalid Path - `/api/v1/diffs/generate`
- **Line 64**: Invalid Path - `/api/v1/diffs/status/`
- **Line 79**: Invalid Path - `/api/v1/diffs/`
- **Line 17**: Invalid Command - `just demo-diff-generation`

### docs/api/graphql.md

- **Line 154**: Invalid Path - `conf/.../graphql.yaml`
- **Line 187**: Invalid Path - `tests/integration/api/`
- **Line 195**: Invalid Path - `create/update`

### docs/api/index.md

- **Line 10**: Invalid Path - `request/response`
- **Line 19**: Invalid Path - `//api.haven.local/api/v1`
- **Line 24**: Invalid Path - `//api.haven.local/api/v1/records`
- **Line 41**: Invalid Path - `//api.haven.local/graphql`
- **Line 94**: Invalid Path - `requests/hour`
- **Line 95**: Invalid Path - `queries/hour`
- **Line 112**: Invalid Path - `/api/v1/`
- **Line 112**: Invalid Path - `/api/v2/`

### docs/api/openapi.md

- **Line 66**: Invalid Path - `src/haven/interface/api/app.py`
- **Line 8**: Invalid Path - `//api.haven.local/docs`
- **Line 11**: Invalid Path - `//api.haven.local/redoc`
- **Line 15**: Invalid Path - `//api.haven.local/openapi.json`
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

### docs/api/rest.md

- **Line 220**: Invalid Path - `value_error.missing`
- **Line 292**: Invalid Path - `record.created`
- **Line 12**: Invalid Path - `//api.haven.local/api/v1`
- **Line 15**: Invalid Path - `/api/v1`
- **Line 32**: Invalid Path - `application/json`
- **Line 89**: Invalid Path - `/api/v1/records`
- **Line 117**: Invalid Path - `/api/v1/records/`
- **Line 196**: Invalid Path - `/data/key`
- **Line 197**: Invalid Path - `/data/new_field`
- **Line 308**: Invalid Path - `//api.haven.local/api/v1/records`
- **Line 313**: Invalid Path - `//api.haven.local/api/v1/records/550e8400-e29b-41d4-a716-446655440000`
- **Line 320**: Invalid Path - `//api.haven.local`
- **Line 342**: Invalid Command - `just docs`

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
- **Line 51**: Invalid Command - `just database::up`
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
- **Line 56**: Invalid Command - `just database::up`
- **Line 58**: Invalid Command - `just database::make "<message>"`
- **Line 60**: Invalid Command - `just database::migrate`
- **Line 71**: Invalid Command - `just database::make`
- **Line 152**: Invalid Command - `just database::migrate-prod`
- **Line 191**: Invalid Command - `just database::migrate-offline`
- **Line 227**: Invalid Command - `just database::migrate`

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
- **Line 20**: Invalid Path - `//web.haven.local`
- **Line 21**: Invalid Path - `//localhost`
- **Line 22**: Invalid Path - `//api.haven.local`
- **Line 23**: Invalid Path - `//app.haven.local`
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
- **Line 21**: Localhost Url - `http://localhost:5173` → `http://haven.local:5173`
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
- **Line 93**: Invalid Command - `just docker::up`
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
- **Line 142**: Invalid Command - `just docker::up`
- **Line 143**: Invalid Command - `just database::up`
- **Line 144**: Invalid Command - `just database::migrate`

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
- **Line 81**: Invalid Command - `just database::migrate`
- **Line 81**: Invalid Command - `just testing::python  # Delegates to apps/api/justfile`

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
- **Line 77**: Invalid Path - `//api.haven.local`
- **Line 79**: Invalid Path - `//api.haven.local/docs`
- **Line 80**: Invalid Path - `//api.haven.local/graphql`
- **Line 102**: Invalid Path - `create/update`
- **Line 21**: Invalid Command - `just database::up          # see § 3 for details`
- **Line 63**: Invalid Command - `just database::up           # spin up Postgres (+ OTel if enabled)`
- **Line 63**: Invalid Command - `just db-down         # stop and remove the compose stack`
- **Line 63**: Invalid Command - `just database::migrate      # apply Alembic migrations to the running DB`
- **Line 128**: Invalid Command - `just db-down     # stop containers`
- **Line 120**: Invalid Command - `just claude`

### docs/development/migration-strategies.md

- **Line 43**: Invalid Path - `CI/CD`
- **Line 8**: Invalid Command - `just database::migrate`
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
- **Line 127**: Invalid Command - `just database::reset`
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
- **Line 118**: Invalid Path - `//api.haven.local`
- **Line 127**: Invalid Path - `tests/e2e`
- **Line 136**: Invalid Path - `setup/teardown.`
- **Line 143**: Invalid Path - `code/api`
- **Line 148**: Invalid Command - `just db-down`

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
- **Line 7**: Invalid Command - `just database::up`
- **Line 7**: Invalid Command - `just database::migrate`
- **Line 7**: Invalid Command - `just demos::ttr`
- **Line 165**: Invalid Command - `just database::console`
- **Line 231**: Invalid Command - `just database::reset`
- **Line 231**: Invalid Command - `just database::current`
- **Line 231**: Invalid Command - `just database::history`
- **Line 243**: Invalid Command - `just testing::coverage`

### docs/documentation-audit-report.md

- **Line 20**: Invalid Path - `docs/architecture.md`
- **Line 21**: Invalid Path - `docs/quality.md`
- **Line 22**: Invalid Path - `docs/definition-of-done.md`
- **Line 23**: Invalid Path - `docs/local-setup.md`
- **Line 24**: Invalid Path - `docs/spec.md`
- **Line 25**: Invalid Path - `docs/tasks-workflow.md`
- **Line 26**: Invalid Path - `docs/alembic.md`
- **Line 27**: Invalid Path - `docs/refactoring.md`
- **Line 28**: Invalid Path - `YYYY-MM-DD.NNNN`
- **Line 29**: Invalid Path - `docs/roadmap.md`
- **Line 30**: Invalid Path - `docs/commits-plan.md`
- **Line 31**: Invalid Path - `//web.haven.local`
- **Line 35**: Invalid Path - `tests/test_api.py`
- **Line 36**: Invalid Path - `tasks/open/feature-name.md`
- **Line 37**: Invalid Path - `docs/workflow-name.md`
- **Line 39**: Invalid Path - `src/interface/api/routes.py`
- **Line 40**: Invalid Path - `tests/interface/api/test_routes.py`
- **Line 41**: Invalid Path - `src/interface/graphql/schema.py`
- **Line 42**: Invalid Path - `src/domain/models.py`
- **Line 47**: Invalid Path - `tests/integration/test_graphql.py`
- **Line 76**: Invalid Path - `//github.com/jazzydog-labs/haven/actions/workflows/ci.yml/badge.svg`
- **Line 77**: Invalid Path - `//github.com/jazzydog-labs/haven/actions/workflows/ci.yml`
- **Line 80**: Invalid Path - `//img.shields.io/badge/License-MIT-yellow.svg`
- **Line 85**: Invalid Path - `//github.com/jazzydog-labs/haven.git`
- **Line 92**: Invalid Path - `tests/unit/domain/test_record.py`
- **Line 98**: Invalid Path - `docs/testing.md`
- **Line 99**: Invalid Path - `docs/deployment.md`
- **Line 108**: Invalid Path - `just test-file tests/unit/domain/test_record.py`
- **Line 149**: Invalid Path - `scripts/demo-diff-generation.py`
- **Line 161**: Invalid Path - `conf/.../graphql.yaml`
- **Line 182**: Invalid Path - `src/haven/interface/api/app.py`
- **Line 186**: Invalid Path - `8080/openapi.json`
- **Line 211**: Invalid Path - `value_error.missing`
- **Line 212**: Invalid Path - `record.created`
- **Line 233**: Invalid Path - `src/domain/entities/record.py`
- **Line 235**: Invalid Path - `src/application/use_cases/create_record.py`
- **Line 237**: Invalid Path - `src/infrastructure/database/repositories/record_repository.py`
- **Line 239**: Invalid Path - `src/interface/api/routes/records.py`
- **Line 260**: Invalid Path - `//semver.org/spec/v2.0.0.html`
- **Line 262**: Invalid Path - `//github.com/jazzydog-labs/haven/compare/main...HEAD`
- **Line 266**: Invalid Path - `//github.com/your-username/haven.git`
- **Line 274**: Invalid Path - `sqlalchemy.ext.asyncio`
- **Line 275**: Invalid Path - `env.py`
- **Line 276**: Invalid Path - `{YYYYMMDD}_{NN}_{slug}.py`
- **Line 277**: Invalid Path - `models.py`
- **Line 279**: Invalid Path - `versions/20250715_02_add_tag_column_to_record.py`
- **Line 282**: Invalid Path - `//alembic.sqlalchemy.org/en/latest/branches.html`
- **Line 283**: Invalid Path - `//alembic.sqlalchemy.org/en/latest/cookbook.html`
- **Line 293**: Invalid Path - `cache/redis.yaml`
- **Line 294**: Invalid Path - `haven.config.settings.AppSettings`
- **Line 295**: Invalid Path - `database/postgres.yaml`
- **Line 296**: Invalid Path - `redis.yaml`
- **Line 297**: Invalid Path - `local.yaml`
- **Line 298**: Invalid Path - `defaults.yaml`
- **Line 304**: Invalid Path - `environment/test.yaml`
- **Line 309**: Invalid Path - `127.0.0.1 api.haven.local`
- **Line 310**: Invalid Path - `127.0.0.1 app.haven.local`
- **Line 311**: Invalid Path - `127.0.0.1 haven.local`
- **Line 313**: Invalid Path - `//app.haven.local`
- **Line 314**: Invalid Path - `//api.haven.local`
- **Line 315**: Invalid Path - `//your-custom-origin.com`
- **Line 316**: Invalid Path - `/scripts/setup-local-domains.sh`
- **Line 320**: Invalid Path - `//haven.local`
- **Line 325**: Invalid Path - `/operations/production-setup.md`
- **Line 337**: Invalid Path - `todo.md`
- **Line 345**: Invalid Path - `justfile.demos`
- **Line 346**: Invalid Path - `/operations/container-troubleshooting.md`
- **Line 367**: Invalid Path - `.env.https`
- **Line 368**: Invalid Path - `Proceed to haven.local`
- **Line 369**: Invalid Path - `myapp.local`
- **Line 370**: Invalid Path - `*.myapp.local`
- **Line 371**: Invalid Path - `api.myapp.local`
- **Line 372**: Invalid Path - `*.local`
- **Line 375**: Invalid Path - `/certs/key.pem`
- **Line 376**: Invalid Path - `/certs/cert.pem`
- **Line 387**: Invalid Path - `justfile.common`
- **Line 394**: Invalid Path - `web.haven.local`
- **Line 395**: Invalid Path - `api.haven.local`
- **Line 396**: Invalid Path - `haven.local`
- **Line 397**: Invalid Path - `app.haven.local`
- **Line 398**: Invalid Path - `/etc/hosts.haven.backup`
- **Line 403**: Invalid Path - `/operations/docker.md`
- **Line 407**: Invalid Path - `docker-compose.yaml`
- **Line 408**: Invalid Path - `Implement pending tasks in todo.md`
- **Line 410**: Invalid Path - `//just.systems`
- **Line 411**: Invalid Path - `jazzydog-labs/haven.git`
- **Line 412**: Invalid Path - `//install.hatch.pm`
- **Line 414**: Invalid Path - `claude/settings.json`
- **Line 446**: Invalid Path - `pyrightconfig.json`
- **Line 456**: Invalid Path - `*.py`
- **Line 462**: Invalid Path - `src/services/everything.py`
- **Line 464**: Invalid Path - `src/api/utils.py`
- **Line 466**: Invalid Path - `src/graphql/utils.py`
- **Line 472**: Invalid Path - `conf/database/postgres.yaml`
- **Line 473**: Invalid Path - `alembic/versions/xxx_add_new_column.py`
- **Line 474**: Invalid Path - `alembic/versions/yyy_copy_data.py`
- **Line 475**: Invalid Path - `alembic/versions/zzz_drop_old_column.py`
- **Line 482**: Invalid Path - `.just/discover-packages.sh`
- **Line 484**: Invalid Path - `just/common.just`
- **Line 485**: Invalid Path - `tools/deploy.just`
- **Line 489**: Invalid Path - `just/help.sh`
- **Line 494**: Invalid Path - `just/completions.sh`
- **Line 495**: Invalid Path - `just/discover-packages.sh`
- **Line 516**: Invalid Path - `tasks/open/user-authentication.md`
- **Line 518**: Invalid Path - `graphql-subscriptions.md`
- **Line 519**: Invalid Path - `tasks/closed/basic-crud-operations.md`
- **Line 520**: Invalid Path - `work-log.md`
- **Line 521**: Invalid Path - `user-authentication.md`
- **Line 522**: Invalid Path - `tasks/open/graphql-pagination.md`
- **Line 523**: Invalid Path - `tasks/open/database-connection-pooling.md`
- **Line 525**: Invalid Path - `tasks/open/task-name.md`
- **Line 527**: Invalid Path - `tasks/open/new-feature.md`
- **Line 528**: Invalid Path - `tasks/open/completed-task.md`
- **Line 532**: Invalid Path - `@pytest.mark.parametrize`
- **Line 533**: Invalid Path - `monkeypatch.setattr`
- **Line 534**: Invalid Path - `tests/conftest.py`
- **Line 535**: Invalid Path - `tests/e2e/smoke_test.py`
- **Line 536**: Invalid Path - `@pytest.mark.slow`
- **Line 551**: Invalid Path - `tests/unit/domain/test_user.py`
- **Line 552**: Invalid Path - `tests/unit/domain/test_repository.py`
- **Line 553**: Invalid Path - `tests/unit/application/test_user_service.py`
- **Line 554**: Invalid Path - `tests/unit/application/test_repository_service.py`
- **Line 555**: Invalid Path - `tests/unit/infrastructure/test_user_repository.py`
- **Line 556**: Invalid Path - `tests/unit/infrastructure/test_repository_repository.py`
- **Line 559**: Invalid Path - `//github.com/user/test-repo.git`
- **Line 578**: Invalid Path - `index.html`
- **Line 579**: Invalid Path - `01-abc12345-commit-message.html`
- **Line 580**: Invalid Path - `diff-output/index.html`
- **Line 606**: Invalid Path - `haven_*.sql.gz`
- **Line 616**: Invalid Path - `/etc/ssl/certs/cert.pem`
- **Line 617**: Invalid Path - `/etc/ssl/private/key.pem`
- **Line 626**: Invalid Path - `/app/.tmp`
- **Line 654**: Invalid Path - `compose.yaml`
- **Line 658**: Invalid Path - `/root/.cache`
- **Line 659**: Invalid Path - `/tmp/req.txt`
- **Line 665**: Invalid Path - `//security.scw.cloud`
- **Line 670**: Invalid Path - `haven.api`
- **Line 671**: Invalid Path - `record.id`
- **Line 672**: Invalid Path - `result.status`
- **Line 695**: Invalid Path - `docs/configuration.md`
- **Line 705**: Invalid Path - `/scripts/demo-commits.sh`
- **Line 734**: Invalid Path - `mkdir -p .claude`
- **Line 735**: Invalid Path - `guardrails/checklist.yaml`
- **Line 736**: Invalid Path - `Create the Stop and PreToolUse hooks described in SPEC.md`
- **Line 769**: Invalid Path - `conf/{environment}/{component}.yaml`
- **Line 793**: Invalid Path - `docs/docker.md`
- **Line 818**: Invalid Path - `/apps/api/.venv`
- **Line 819**: Invalid Path - `/app/.venv`
- **Line 826**: Invalid Path - `types/record.ts`
- **Line 827**: Invalid Path - `services/api/records.ts`
- **Line 838**: Invalid Path - `apps/web/src/types/domain.ts`
- **Line 841**: Invalid Path - `github/workflows/api-compatibility.yml`
- **Line 845**: Invalid Path - `/scripts/sync-frontend-backend.sh`
- **Line 846**: Invalid Path - `apps/api/openapi.json`
- **Line 847**: Invalid Path - `/scripts/generate-crud.sh`
- **Line 879**: Invalid Path - `/etc/nginx/certs/cert.pem`
- **Line 880**: Invalid Path - `/etc/nginx/certs/key.pem`
- **Line 884**: Invalid Path - `//api.production.com`
- **Line 906**: Invalid Path - `src/haven/domain/entities/comment.py`
- **Line 907**: Invalid Path - `src/haven/infrastructure/database/models/comment.py`
- **Line 908**: Invalid Path - `src/haven/application/services/comment_service.py`
- **Line 909**: Invalid Path - `src/haven/domain/repositories/comment_repository.py`
- **Line 910**: Invalid Path - `tests/unit/domain/entities/test_comment.py`
- **Line 911**: Invalid Path - `tests/unit/application/services/test_comment_service.py`
- **Line 912**: Invalid Path - `commits.id`
- **Line 913**: Invalid Path - `users.id`
- **Line 914**: Invalid Path - `src/main.py`
- **Line 919**: Invalid Path - `src/haven/domain/entities/repository.py`
- **Line 920**: Invalid Path - `src/haven/infrastructure/database/models/repository.py`
- **Line 921**: Invalid Path - `src/haven/application/services/repository_service.py`
- **Line 922**: Invalid Path - `tests/unit/domain/entities/test_repository.py`
- **Line 923**: Invalid Path - `github.com`
- **Line 926**: Invalid Path - `//github.com/user/test.git`
- **Line 931**: Invalid Path - `src/haven/domain/entities/user.py`
- **Line 932**: Invalid Path - `src/haven/infrastructure/database/models/user.py`
- **Line 933**: Invalid Path - `tests/unit/domain/entities/test_user.py`
- **Line 971**: Invalid Path - `/etc/traefik/traefik.yml`
- **Line 977**: Invalid Path - `src/haven/domain/entities/commit.py`
- **Line 978**: Invalid Path - `src/haven/infrastructure/database/models/commit.py`
- **Line 979**: Invalid Path - `src/haven/application/services/commit_service.py`
- **Line 980**: Invalid Path - `tests/unit/domain/entities/test_commit.py`
- **Line 981**: Invalid Path - `repositories.id`
- **Line 988**: Invalid Path - `tasks/open/frontend-backend-sync-workflow.md`
- **Line 989**: Invalid Path - `implement-scalable-justfile-system.md`
- **Line 990**: Invalid Path - `comprehensive-docs-audit.md`
- **Line 991**: Invalid Path - `crud-frontend-records.md`
- **Line 992**: Invalid Path - `frontend-backend-sync-workflow.md`
- **Line 993**: Invalid Path - `local-https-setup.md`
- **Line 994**: Invalid Path - `production-like-local-env.md`
- **Line 1003**: Invalid Path - `src/haven/infrastructure/database/repositories/repository_repository.py`
- **Line 1004**: Invalid Path - `just test tests/unit/domain/test_repository.py tests/unit/infrastructure/test_repository_repository.py tests/unit/application/test_repository_service.py`
- **Line 1006**: Invalid Path - `src/haven/infrastructure/database/repositories/user_repository.py`
- **Line 1007**: Invalid Path - `just test tests/unit/domain/test_user.py tests/unit/infrastructure/test_user_repository.py tests/unit/application/test_user_service.py`
- **Line 1009**: Invalid Path - `sudo ./scripts/setup-local-domains.sh`
- **Line 1028**: Invalid Path - `apps/api/htmlcov/index.html`
- **Line 1128**: Invalid Path - `apps/web/src/types/openapi.prev.json`
- **Line 1142**: Invalid Path - `consistency-report.md`
- **Line 1143**: Invalid Path - `scripts/generate-consistency-report.py`
- **Line 1144**: Invalid Path - `tests/test_documentation.py`
- **Line 1145**: Invalid Path - `requirements-docs.txt`
- **Line 1146**: Invalid Path - `scripts/fix-common-issues.py`
- **Line 1147**: Invalid Path - `scripts/check-external-links.py`
- **Line 1153**: Invalid Path - `github/workflows/docs-check.yml`
- **Line 32**: Invalid Path - `//api.haven.local/docs`
- **Line 33**: Invalid Path - `//api.haven.local/graphql`
- **Line 34**: Invalid Path - `roadmap/todo`
- **Line 38**: Invalid Path - `Tools/Commands`
- **Line 43**: Invalid Path - `linting/typing`
- **Line 44**: Invalid Path - `Python/Node`
- **Line 45**: Invalid Path - `added/changed`
- **Line 46**: Invalid Path - `feature/fix`
- **Line 48**: Invalid Path - `tasks/closed/`
- **Line 49**: Invalid Path - `/docs/project-management/`
- **Line 78**: Invalid Path - `//img.shields.io/badge/python-3.12`
- **Line 79**: Invalid Path - `//www.python.org/downloads/`
- **Line 81**: Invalid Path - `//opensource.org/licenses/MIT`
- **Line 82**: Invalid Path - `//img.shields.io/badge/code`
- **Line 83**: Invalid Path - `//github.com/astral-sh/ruff`
- **Line 84**: Invalid Path - `async/await`
- **Line 86**: Invalid Path - `//localhost`
- **Line 87**: Invalid Path - `8080/docs`
- **Line 88**: Invalid Path - `8080/graphql`
- **Line 89**: Invalid Path - `8080/health`
- **Line 90**: Invalid Path - `src/haven/`
- **Line 91**: Invalid Path - `//github.com/casey/just`
- **Line 93**: Invalid Path - `8080/api/v1/records`
- **Line 94**: Invalid Path - `application/json`
- **Line 95**: Invalid Path - `//jazzydog-labs.github.io/haven`
- **Line 100**: Invalid Path - `//fastapi.tiangolo.com/`
- **Line 101**: Invalid Path - `//strawberry.rocks/`
- **Line 102**: Invalid Path - `//www.sqlalchemy.org/`
- **Line 103**: Invalid Path - `//pydantic-docs.helpmanual.io/`
- **Line 104**: Invalid Path - `//hydra.cc/`
- **Line 140**: Invalid Path - `8080/api/`
- **Line 151**: Invalid Path - `8080/api/v1/diffs/generate`
- **Line 153**: Invalid Path - `/api/v1/diffs/generate`
- **Line 154**: Invalid Path - `/api/v1/diffs/status/`
- **Line 155**: Invalid Path - `/api/v1/diffs/`
- **Line 162**: Invalid Path - `tests/integration/api/`
- **Line 163**: Invalid Path - `create/update`
- **Line 167**: Invalid Path - `request/response`
- **Line 169**: Invalid Path - `8080/api/v1`
- **Line 172**: Invalid Path - `requests/hour`
- **Line 173**: Invalid Path - `queries/hour`
- **Line 174**: Invalid Path - `/api/v1/`
- **Line 175**: Invalid Path - `/api/v2/`
- **Line 185**: Invalid Path - `8080/redoc`
- **Line 187**: Invalid Path - `Request/response`
- **Line 188**: Invalid Path - `openapitools/openapi-generator-cli`
- **Line 189**: Invalid Path - `Import/Export`
- **Line 191**: Invalid Path - `/api/v1/records`
- **Line 193**: Invalid Path - `/components/schemas/RecordListResponseDTO`
- **Line 194**: Invalid Path - `stoplight/spectral-cli`
- **Line 196**: Invalid Path - `//swagger.io/specification/`
- **Line 215**: Invalid Path - `/api/v1`
- **Line 218**: Invalid Path - `/api/v1/records/`
- **Line 219**: Invalid Path - `/data/key`
- **Line 220**: Invalid Path - `/data/new_field`
- **Line 222**: Invalid Path - `8080/api/v1/records/550e8400-e29b-41d4-a716-446655440000`
- **Line 232**: Invalid Path - `src/domain/`
- **Line 234**: Invalid Path - `src/application/`
- **Line 236**: Invalid Path - `src/infrastructure/`
- **Line 238**: Invalid Path - `src/interface/`
- **Line 240**: Invalid Path - `read/write`
- **Line 244**: Invalid Path - `jazzydog-labs/haven`
- **Line 245**: Invalid Path - `text/content`
- **Line 246**: Invalid Path - `reviewed/needs`
- **Line 247**: Invalid Path - `Edit/delete`
- **Line 248**: Invalid Path - `Add/remove`
- **Line 249**: Invalid Path - `/api/v1/repositories`
- **Line 250**: Invalid Path - `id/sync`
- **Line 251**: Invalid Path - `/api/v1/commits`
- **Line 252**: Invalid Path - `id/diff`
- **Line 253**: Invalid Path - `/api/v1/reviews`
- **Line 254**: Invalid Path - `/api/v1/comments`
- **Line 255**: Invalid Path - `/api/v1/users`
- **Line 259**: Invalid Path - `//keepachangelog.com/en/1.0.0/`
- **Line 261**: Invalid Path - `CI/CD`
- **Line 268**: Invalid Path - `feature/your-feature-name`
- **Line 278**: Invalid Path - `src/haven/infrastructure/database/`
- **Line 280**: Invalid Path - `migrations/archive/`
- **Line 299**: Invalid Path - `environment/local`
- **Line 300**: Invalid Path - `database/postgres`
- **Line 301**: Invalid Path - `logging/default`
- **Line 302**: Invalid Path - `//haven`
- **Line 303**: Invalid Path - `5432/haven`
- **Line 305**: Invalid Path - `//hydra.cc/docs/intro/`
- **Line 317**: Invalid Path - `macOS/Linux`
- **Line 321**: Invalid Path - `//haven.local/api`
- **Line 322**: Invalid Path - `//haven.local/graphql`
- **Line 323**: Invalid Path - `//haven.local/docs`
- **Line 324**: Invalid Path - `//127.0.0.1`
- **Line 377**: Invalid Path - `/etc/nginx`
- **Line 378**: Invalid Path - `/etc/nginx/certs`
- **Line 379**: Invalid Path - `//api.haven.local/api/v1`
- **Line 380**: Invalid Path - `Chrome/Edge`
- **Line 381**: Invalid Path - `//haven.local/auth/callback`
- **Line 382**: Invalid Path - `SSL/TLS`
- **Line 383**: Invalid Path - `/dev-certs/certs`
- **Line 388**: Invalid Path - `js/TypeScript`
- **Line 389**: Invalid Path - `deployment/release`
- **Line 409**: Invalid Path - `//github.com/pyenv/pyenv`
- **Line 413**: Invalid Path - `anthropic-ai/claude-code`
- **Line 415**: Invalid Path - `local/pgdata`
- **Line 447**: Invalid Path - `module/docstring`
- **Line 448**: Invalid Path - `//github.com/astral`
- **Line 449**: Invalid Path - `sh/ruff`
- **Line 450**: Invalid Path - `//github.com/microsoft/pyright`
- **Line 457**: Invalid Path - `s/src.old.path/src.new.path/g`
- **Line 458**: Invalid Path - `src/new/path`
- **Line 459**: Invalid Path - `src/old/path/`
- **Line 460**: Invalid Path - `src/new/path/`
- **Line 461**: Invalid Path - `github/workflows/`
- **Line 463**: Invalid Path - `src/services/`
- **Line 465**: Invalid Path - `src/common/`
- **Line 467**: Invalid Path - `conf/new_structure/`
- **Line 468**: Invalid Path - `conf/old_group`
- **Line 469**: Invalid Path - `conf/new_structure/group`
- **Line 470**: Invalid Path - `new_structure/group`
- **Line 471**: Invalid Path - `//...`
- **Line 477**: Invalid Path - `/api/v2/records`
- **Line 483**: Invalid Path - `recipes/variables`
- **Line 486**: Invalid Path - `packages/api-gateway/justfile`
- **Line 487**: Invalid Path - `packages/auth-service/justfile`
- **Line 488**: Invalid Path - `packages/web-app/justfile`
- **Line 490**: Invalid Path - `y/N`
- **Line 491**: Invalid Path - `js/Express`
- **Line 492**: Invalid Path - `Python/FastAPI`
- **Line 493**: Invalid Path - `React/TypeScript`
- **Line 497**: Invalid Path - `templates/node-service`
- **Line 498**: Invalid Path - `templates/python-service`
- **Line 524**: Invalid Path - `login/logout`
- **Line 538**: Invalid Path - `tests/unit`
- **Line 539**: Invalid Path - `print/debug`
- **Line 540**: Invalid Path - `conf/test`
- **Line 542**: Invalid Path - `tests/e2e`
- **Line 543**: Invalid Path - `setup/teardown.`
- **Line 544**: Invalid Path - `code/api`
- **Line 558**: Invalid Path - `user/test-repo`
- **Line 567**: Invalid Path - `Async/await`
- **Line 568**: Invalid Path - `OpenAPI/Swagger`
- **Line 570**: Invalid Path - `//github.com/jazzydog-labs/haven/issues`
- **Line 571**: Invalid Path - `//github.com/jazzydog-labs/haven/discussions`
- **Line 595**: Invalid Path - `/app/src`
- **Line 596**: Invalid Path - `/apps/api`
- **Line 597**: Invalid Path - `/apps/api/src`
- **Line 598**: Invalid Path - `/Users/name/project`
- **Line 601**: Invalid Path - `//api`
- **Line 607**: Invalid Path - `com/haven`
- **Line 608**: Invalid Path - `/var/lib/postgresql/data`
- **Line 609**: Invalid Path - `apps/v1`
- **Line 610**: Invalid Path - `//user`
- **Line 611**: Invalid Path - `5432/dbname`
- **Line 612**: Invalid Path - `/health/ready`
- **Line 613**: Invalid Path - `/health/live`
- **Line 614**: Invalid Path - `//jaeger`
- **Line 615**: Invalid Path - `HTTPS/TLS`
- **Line 619**: Invalid Path - `BACKUP_DIR/haven_`
- **Line 620**: Invalid Path - `deployment/haven`
- **Line 621**: Invalid Path - `I/O`
- **Line 629**: Invalid Path - `/apps/api/conf`
- **Line 630**: Invalid Path - `/app/conf`
- **Line 631**: Invalid Path - `/apps/api/alembic`
- **Line 632**: Invalid Path - `/app/alembic`
- **Line 633**: Invalid Path - `/apps/api/logs`
- **Line 634**: Invalid Path - `/app/logs`
- **Line 635**: Invalid Path - `/apps/api/tests`
- **Line 636**: Invalid Path - `/app/tests`
- **Line 655**: Invalid Path - `dev/chainguard/python`
- **Line 656**: Invalid Path - `linux/arm64`
- **Line 657**: Invalid Path - `linux/amd64`
- **Line 660**: Invalid Path - `/usr/local/lib/python3.12/site-packages`
- **Line 662**: Invalid Path - `//github.com/jazzydog-labs/haven`
- **Line 663**: Invalid Path - `/app/out/`
- **Line 664**: Invalid Path - `/sbin/tini`
- **Line 666**: Invalid Path - `//github.com/chainguard-images`
- **Line 675**: Invalid Path - `8080/metrics`
- **Line 680**: Invalid Path - `8080/admin/debug`
- **Line 681**: Invalid Path - `created/updated`
- **Line 704**: Invalid Path - `TypeScript/React`
- **Line 706**: Invalid Path - `venv/bin/python`
- **Line 739**: Invalid Path - `//docs.anthropic.com/en/docs/claude-code/setup`
- **Line 740**: Invalid Path - `//docs.anthropic.com/en/docs/claude-code/iam`
- **Line 741**: Invalid Path - `//docs.anthropic.com/en/docs/claude-code/security`
- **Line 742**: Invalid Path - `//docs.anthropic.com/en/docs/claude-code/hooks`
- **Line 743**: Invalid Path - `//docs.anthropic.com/en/docs/claude-code/cli-reference`
- **Line 744**: Invalid Path - `//docs.anthropic.com/en/docs/claude-code/quickstart`
- **Line 745**: Invalid Path - `//docs.anthropic.com/en/docs/claude-code/interactive-mode`
- **Line 752**: Invalid Path - `Python/TypeScript`
- **Line 753**: Invalid Path - `requests/responses`
- **Line 754**: Invalid Path - `schema/resolvers`
- **Line 755**: Invalid Path - `queries/mutations`
- **Line 761**: Invalid Path - `Prometheus/Grafana`
- **Line 762**: Invalid Path - `REST/GraphQL`
- **Line 763**: Invalid Path - `OpenAPI/GraphQL`
- **Line 771**: Invalid Path - `conf/local`
- **Line 772**: Invalid Path - `query/mutation`
- **Line 773**: Invalid Path - `up/down`
- **Line 774**: Invalid Path - `docs/adr/`
- **Line 775**: Invalid Path - `Authentication/authorization`
- **Line 790**: Invalid Path - `Proxy/firewall`
- **Line 792**: Invalid Path - `macOS/Linux/Windows`
- **Line 808**: Invalid Path - `start/stop`
- **Line 823**: Invalid Path - `Search/filter`
- **Line 824**: Invalid Path - `Create/Edit`
- **Line 825**: Invalid Path - `modal/page`
- **Line 839**: Invalid Path - `apps/web/src/services/api/generated`
- **Line 842**: Invalid Path - `actions/checkout`
- **Line 843**: Invalid Path - `oasdiff/oasdiff-action`
- **Line 844**: Invalid Path - `origin/main`
- **Line 848**: Invalid Path - `githooks/pre-commit`
- **Line 849**: Invalid Path - `domain/entities`
- **Line 850**: Invalid Path - `interface/api`
- **Line 851**: Invalid Path - `Add/modify`
- **Line 863**: Invalid Path - `dev/staging/prod`
- **Line 865**: Invalid Path - `pros/cons`
- **Line 877**: Invalid Path - `Docker/FastAPI`
- **Line 878**: Invalid Path - `/etc/caddy/Caddyfile`
- **Line 882**: Invalid Path - `cameronhunter/local-ssl-proxy`
- **Line 888**: Invalid Path - `build/test/deployment`
- **Line 890**: Invalid Path - `import/inclusion`
- **Line 891**: Invalid Path - `api/justfile`
- **Line 892**: Invalid Path - `client/justfile`
- **Line 902**: Invalid Path - `Example/demo`
- **Line 925**: Invalid Path - `user/test`
- **Line 934**: Invalid Path - `dataclass/model`
- **Line 941**: Invalid Path - `migrations/models`
- **Line 943**: Invalid Path - `8080/5432`
- **Line 955**: Invalid Path - `output/feedback`
- **Line 956**: Invalid Path - `success/failure`
- **Line 973**: Invalid Path - `Traefik/Caddy`
- **Line 1012**: Invalid Path - `8080/api/v1/ttr/tasks`
- **Line 1015**: Invalid Path - `tasks/milestones`
- **Line 1019**: Invalid Path - `venv/bin/activate`
- **Line 1026**: Invalid Path - `8080/api/v1/diffs/status/`
- **Line 1027**: Invalid Path - `tmp/diff-output/diff-out-`
- **Line 1029**: Invalid Path - `tmp/diff-output/`
- **Line 1032**: Invalid Path - `macOS/Windows/Linux`
- **Line 1033**: Invalid Path - `printing/bookmarking`
- **Line 1038**: Invalid Path - `//haven.local/api/v1/records`
- **Line 1039**: Invalid Path - `//haven.local/health`
- **Line 1040**: Invalid Path - `Create/edit`
- **Line 1041**: Invalid Path - `loading/error`
- **Line 1045**: Invalid Path - `add/remove`
- **Line 1109**: Invalid Path - `8080/api/v1/records/`
- **Line 1133**: Invalid Path - `hey-api/openapi-ts`
- **Line 1149**: Invalid Path - `fix/critical-docs-issues`
- **Line 1150**: Invalid Path - `fix/important-docs-updates`
- **Line 1151**: Invalid Path - `fix/minor-docs-cleanup`
- **Line 1154**: Invalid Path - `weekly/monthly`
- **Line 1155**: Invalid Path - `compile/run`
- **Line 1156**: Invalid Path - `movements/renames`
- **Line 50**: Invalid Command - `just database::up     # Start PostgreSQL`
- **Line 51**: Invalid Command - `just testing::fast    # Run unit tests only (quick feedback)`
- **Line 52**: Invalid Command - `just api::add-entity User`
- **Line 53**: Invalid Command - `just database::make "add_users_table" && just database::migrate`
- **Line 54**: Invalid Command - `just database::make "add_status_to_items"`
- **Line 55**: Invalid Command - `just database::console`
- **Line 56**: Invalid Command - `just shell`
- **Line 57**: Invalid Command - `just docker::up-d      # Start all services in background`
- **Line 58**: Invalid Command - `just docker::down      # Stop all services`
- **Line 59**: Invalid Command - `just docker::logs api  # View API logs`
- **Line 60**: Invalid Command - `just docker::shell     # Shell into API container`
- **Line 61**: Invalid Command - `just database::migrate-docker             # Run migrations in Docker`
- **Line 62**: Invalid Command - `just database::make-docker "add_users"   # Create migration in Docker`
- **Line 63**: Invalid Command - `just database::console-docker             # Database console via Docker`
- **Line 64**: Invalid Command - `just docker::test      # Run tests in container`
- **Line 65**: Invalid Command - `just docker::lint      # Run linting in container`
- **Line 66**: Invalid Command - `just docker::type-check # Type checking in container`
- **Line 67**: Invalid Command - `just docker::ps        # Show running containers`
- **Line 68**: Invalid Command - `just docker::rebuild   # Rebuild containers`
- **Line 69**: Invalid Command - `just docker::reset     # Full reset (data loss!)`
- **Line 70**: Invalid Command - `just --list`
- **Line 71**: Invalid Command - `just docker::up`
- **Line 72**: Invalid Command - `just database::migrate`
- **Line 105**: Invalid Command - `just --list      # Show all available commands`
- **Line 106**: Invalid Command - `just docs-serve  # Preview documentation locally`
- **Line 107**: Invalid Command - `just docker-build # Build Docker image`
- **Line 108**: Invalid Command - `just test-file tests/unit/domain/test_record.py`
- **Line 109**: Invalid Command - `just testing::coverage`
- **Line 129**: Invalid Command - `just type-python      # Type checking`
- **Line 130**: Invalid Command - `just format-python    # Format code`
- **Line 156**: Invalid Command - `just demo-diff-generation`
- **Line 223**: Invalid Command - `just docs`
- **Line 269**: Invalid Command - `just testing::coverage`
- **Line 284**: Invalid Command - `just database::make "add tag column to record"`
- **Line 285**: Invalid Command - `just database::downgrade 1`
- **Line 286**: Invalid Command - `just database::make "<message>"`
- **Line 287**: Invalid Command - `just database::make`
- **Line 288**: Invalid Command - `just database::migrate-prod`
- **Line 289**: Invalid Command - `just database::migrate-offline`
- **Line 340**: Invalid Command - `just docs   # Build documentation`
- **Line 341**: Invalid Command - `just docs`
- **Line 347**: Invalid Command - `just demos::health`
- **Line 348**: Invalid Command - `just demos::api`
- **Line 349**: Invalid Command - `just demos::all`
- **Line 350**: Invalid Command - `just demos::docker`
- **Line 351**: Invalid Command - `just demos::graphql`
- **Line 352**: Invalid Command - `just demos::migrations`
- **Line 353**: Invalid Command - `just demo-<feature>`
- **Line 354**: Invalid Command - `just demos::health`
- **Line 355**: Invalid Command - `just demos::api`
- **Line 356**: Invalid Command - `just demos::graphql`
- **Line 357**: Invalid Command - `just demos::docker`
- **Line 358**: Invalid Command - `just demos::migrations`
- **Line 359**: Invalid Command - `just demo-commits`
- **Line 360**: Invalid Command - `just demo-diff-generation`
- **Line 361**: Invalid Command - `just demos::all`
- **Line 362**: Invalid Command - `just demo-commits-docker`
- **Line 363**: Invalid Command - `just demo-diff-generation-docker`
- **Line 420**: Invalid Command - `just db-down         # stop and remove the compose stack`
- **Line 421**: Invalid Command - `just db-down     # stop containers`
- **Line 422**: Invalid Command - `just claude`
- **Line 430**: Invalid Command - `just database::migrate-docker`
- **Line 431**: Invalid Command - `just database::migrate-run`
- **Line 432**: Invalid Command - `just database::migrate-service`
- **Line 433**: Invalid Command - `just database::make "add_user_table"`
- **Line 434**: Invalid Command - `just database::make-docker "add_user_table"`
- **Line 435**: Invalid Command - `just database::history`
- **Line 436**: Invalid Command - `just database::history-docker`
- **Line 437**: Invalid Command - `just database::current`
- **Line 438**: Invalid Command - `just database::current-docker`
- **Line 439**: Invalid Command - `just database::downgrade`
- **Line 440**: Invalid Command - `just database::downgrade-docker`
- **Line 441**: Invalid Command - `just database::reset-docker`
- **Line 451**: Invalid Command - `just lint‑fix        # ruff check --fix . && ruff format .`
- **Line 452**: Invalid Command - `just docs`
- **Line 478**: Invalid Command - `just grep "from src.old.path import"`
- **Line 499**: Invalid Command - `just list-all          List all available commands`
- **Line 500**: Invalid Command - `just cd <path>         Show commands for specific directory`
- **Line 501**: Invalid Command - `just build             Build all packages`
- **Line 502**: Invalid Command - `just watch             Watch all services (opens tmux)`
- **Line 503**: Invalid Command - `just api::dev             # Start only API in dev mode`
- **Line 504**: Invalid Command - `just test-all             # Run all tests`
- **Line 505**: Invalid Command - `just test::integration    # Run integration tests`
- **Line 506**: Invalid Command - `just api::test-file user  # Test specific file`
- **Line 507**: Invalid Command - `just docker::up           # Start containers`
- **Line 508**: Invalid Command - `just docker::logs api     # Show API logs`
- **Line 509**: Invalid Command - `just docker::exec db psql # Access database`
- **Line 510**: Invalid Command - `just deploy::staging      # Deploy to staging`
- **Line 511**: Invalid Command - `just deploy::production   # Deploy to production`
- **Line 545**: Invalid Command - `just db-down`
- **Line 560**: Invalid Command - `just demos::ttr`
- **Line 561**: Invalid Command - `just database::current`
- **Line 562**: Invalid Command - `just database::history`
- **Line 563**: Invalid Command - `just testing::coverage`
- **Line 582**: Invalid Command - `just cli-list-commits                    # List commits`
- **Line 583**: Invalid Command - `just cli-generate                       # Generate diffs`
- **Line 584**: Invalid Command - `just cli-generate-to /path/to/output    # Generate to specific directory`
- **Line 585**: Invalid Command - `just demo-commits           # Full demo with auto-server startup`
- **Line 586**: Invalid Command - `just demo-diff-generation   # Uses API server (requires manual startup)`
- **Line 641**: Invalid Command - `just docker::reset             # Full reset (removes data)`
- **Line 642**: Invalid Command - `just docker::shell             # Shell into API container`
- **Line 643**: Invalid Command - `just database::console-docker        # PostgreSQL console`
- **Line 644**: Invalid Command - `just docker::test              # Run tests in container`
- **Line 645**: Invalid Command - `just docker::lint              # Run linting in container`
- **Line 646**: Invalid Command - `just clean-docker                             # Project cleanup`
- **Line 707**: Invalid Command - `just type-python       # Python type checking`
- **Line 708**: Invalid Command - `just check-python      # All Python quality gates`
- **Line 709**: Invalid Command - `just check-web         # All TypeScript quality gates`
- **Line 710**: Invalid Command - `just docs              # Build documentation`
- **Line 711**: Invalid Command - `just demo-commits      # Demo git diff viewer (auto-starts server)`
- **Line 712**: Invalid Command - `just demo-diff-generation  # Demo git diff API (requires server)`
- **Line 713**: Invalid Command - `just --list            # Show all available commands`
- **Line 714**: Invalid Command - `just cli-list-commits          # List commits via Just command`
- **Line 715**: Invalid Command - `just cli-generate             # Generate HTML diffs via Just command`
- **Line 716**: Invalid Command - `just cli-generate-to /path    # Generate diffs to specific directory`
- **Line 746**: Invalid Command - `just implement`
- **Line 747**: Invalid Command - `just plan "Add Tag entity"`
- **Line 748**: Invalid Command - `just implement`
- **Line 777**: Invalid Command - `just docs`
- **Line 778**: Invalid Command - `just install`
- **Line 779**: Invalid Command - `just docs`
- **Line 780**: Invalid Command - `just build`
- **Line 781**: Invalid Command - `just docs`
- **Line 782**: Invalid Command - `just install && just database::up && just run`
- **Line 896**: Invalid Command - `just demo-*`
- **Line 897**: Invalid Command - `just api:test`
- **Line 915**: Invalid Command - `just database::make "create_comments_table"`
- **Line 927**: Invalid Command - `just database::make "create_repositories_table"`
- **Line 935**: Invalid Command - `just database::make "create_users_table"`
- **Line 944**: Invalid Command - `just run-api-docker         # Start API with hot-reload`
- **Line 945**: Invalid Command - `just database::migrate-docker`
- **Line 946**: Invalid Command - `just database::make "add_user_table"    # Generate migration`
- **Line 947**: Invalid Command - `just database::migrate-docker           # Apply migrations`
- **Line 948**: Invalid Command - `just database::make-docker "add_field"  # Generate in container`
- **Line 957**: Invalid Command - `just demo-*`
- **Line 958**: Invalid Command - `just demo-*`
- **Line 959**: Invalid Command - `just demo-<feature-name>`
- **Line 960**: Invalid Command - `just demos::all`
- **Line 961**: Invalid Command - `just demo-diffs`
- **Line 962**: Invalid Command - `just demos::graphql`
- **Line 963**: Invalid Command - `just demos::api`
- **Line 964**: Invalid Command - `just demos::health`
- **Line 984**: Invalid Command - `just database::make "create_commits_and_reviews_tables"`
- **Line 1048**: Invalid Command - `just check-python # Python lint + type + test (was missing)`
- **Line 1049**: Invalid Command - `just check-web   # Web lint + type + test (was missing)`
- **Line 1050**: Invalid Command - `just demos::docker`
- **Line 1051**: Invalid Command - `just demos::health`
- **Line 1052**: Invalid Command - `just docker::test`
- **Line 1053**: Invalid Command - `just database::console-docker`
- **Line 1054**: Invalid Command - `just testing::coverage`
- **Line 1055**: Invalid Command - `just demos::api`
- **Line 1056**: Invalid Command - `just demos::graphql`
- **Line 1057**: Invalid Command - `just demos::migrations`
- **Line 1058**: Invalid Command - `just database::current-docker`
- **Line 1059**: Invalid Command - `just database::migrate-run`
- **Line 1060**: Invalid Command - `just --list | grep db-.*-docker`
- **Line 1061**: Invalid Command - `just docker::reset`
- **Line 1062**: Invalid Command - `just demos::health      # Health endpoints`
- **Line 1063**: Invalid Command - `just demos::api         # REST CRUD operations`
- **Line 1064**: Invalid Command - `just demos::graphql     # GraphQL queries`
- **Line 1065**: Invalid Command - `just demos::docker      # Container status`
- **Line 1066**: Invalid Command - `just demos::migrations  # Migration strategies`
- **Line 1067**: Invalid Command - `just demos::all`
- **Line 1068**: Invalid Command - `just demos::cors`
- **Line 1069**: Invalid Command - `just demos::sync`
- **Line 1070**: Invalid Command - `just check-api-compat`
- **Line 1071**: Invalid Command - `just demos::https`
- **Line 1072**: Invalid Command - `just --list         # All commands`
- **Line 1073**: Invalid Command - `just docker::help   # Module help`
- **Line 1074**: Invalid Command - `just testing::all   # Module commands`
- **Line 1075**: Invalid Command - `just database::up        # Start PostgreSQL`
- **Line 1076**: Invalid Command - `just docker::logs api    # View API logs`
- **Line 1077**: Invalid Command - `just testing::python     # Run Python tests`
- **Line 1078**: Invalid Command - `just demos::all          # Run all demos`
- **Line 1079**: Invalid Command - `just docker::test`
- **Line 1080**: Invalid Command - `just --list`
- **Line 1081**: Invalid Command - `just docker::test`
- **Line 1082**: Invalid Command - `just database::migrate-docker`
- **Line 1083**: Invalid Command - `just demo-diff-generation`
- **Line 1084**: Invalid Command - `just demo-diff-generation`
- **Line 1085**: Invalid Command - `just database::current-docker`
- **Line 1086**: Invalid Command - `just database::migrate-run`
- **Line 1087**: Invalid Command - `just --list`
- **Line 1088**: Invalid Command - `just demos::all`
- **Line 1089**: Invalid Command - `just demos::cors`
- **Line 1111**: Invalid Command - `just --list`
- **Line 1137**: Invalid Command - `just check-api-compat`
- **Line 1157**: Invalid Command - `just docker::test`
- **Line 110**: Broken Link - [Architecture Overview](docs/architecture.md)
- **Line 111**: Broken Link - [Local Setup Guide](docs/local-setup.md)
- **Line 112**: Broken Link - [Testing Guide](docs/testing.md)
- **Line 113**: Broken Link - [Deployment Guide](docs/deployment.md)
- **Line 270**: Broken Link - [roadmap](roadmap.md)
- **Line 326**: Broken Link - [Local HTTPS Setup](local-https-setup.md)
- **Line 327**: Broken Link - [Production Environment](../operations/production-setup.md)
- **Line 572**: Broken Link - [Architecture Overview](architecture.md)
- **Line 573**: Broken Link - [Development Guide](local-setup.md)
- **Line 574**: Broken Link - [Roadmap](roadmap.md)
- **Line 588**: Broken Link - [Architecture](architecture.md)
- **Line 622**: Broken Link - [Configuration Reference](configuration.md)
- **Line 682**: Broken Link - [Configuration Reference](configuration.md)
- **Line 683**: Broken Link - [Troubleshooting Guide](troubleshooting.md)
- **Line 717**: Broken Link - [`docs/architecture.md`](architecture.md)
- **Line 718**: Broken Link - [`docs/alembic.md`](alembic.md)
- **Line 719**: Broken Link - [`docs/definition-of-done.md`](definition-of-done.md)
- **Line 720**: Broken Link - [`docs/local-setup.md`](local-setup.md)
- **Line 721**: Broken Link - [`docs/testing.md`](testing.md)
- **Line 722**: Broken Link - [`docs/quality.md`](quality.md)
- **Line 723**: Broken Link - [`docs/configuration.md`](configuration.md)
- **Line 724**: Broken Link - [`docs/refactoring.md`](refactoring.md)
- **Line 725**: Broken Link - [`work-log.md`](../work-log.md)
- **Line 726**: Broken Link - [`docs/roadmap.md`](roadmap.md)
- **Line 727**: Broken Link - [`todo.md`](../todo.md)
- **Line 728**: Broken Link - [`docs/spec.md`](spec.md)
- **Line 729**: Broken Link - [`docs/architecture.md`](architecture.md)
- **Line 730**: Broken Link - [`docs/commits-plan.md`](commits-plan.md)
- **Line 1112**: Broken Link - [Architecture Overview](architecture.md)
- **Line 1113**: Broken Link - [Development Environment](local-setup.md)
- **Line 1114**: Broken Link - [Testing](testing.md)
- **Line 1115**: Broken Link - [Code Quality](quality.md)
- **Line 329**: Localhost Url - `http://localhost:5173` → `http://haven.local:5173`
- **Line 333**: Localhost Url - `http://localhost:5173` → `http://haven.local:5173`
- **Line 873**: Localhost Url - `http://localhost:5173` → `http://haven.local:5173`

### docs/documentation-fix-plan.md

- **Line 82**: Invalid Path - `YYYY-MM-DD.NNNN`
- **Line 99**: Invalid Path - `*.md`
- **Line 126**: Invalid Path - `*.bak`
- **Line 59**: Invalid Path - `//web.haven.local`
- **Line 60**: Invalid Path - `//api.haven.local`
- **Line 61**: Invalid Path - `//api.haven.local/docs`
- **Line 62**: Invalid Path - `//api.haven.local/graphql`
- **Line 63**: Invalid Path - `//docs.haven.local`
- **Line 75**: Invalid Path - `src/haven/`
- **Line 81**: Invalid Path - `//github.com/`
- **Line 83**: Invalid Path - `async/await`
- **Line 84**: Invalid Path - `Tools/Commands`
- **Line 99**: Invalid Path - `s/just`
- **Line 99**: Invalid Path - `up/just`
- **Line 99**: Invalid Path - `up/g`
- **Line 100**: Invalid Path - `migrate/just`
- **Line 100**: Invalid Path - `migrate/g`
- **Line 101**: Invalid Path - `console/just`
- **Line 101**: Invalid Path - `console/g`
- **Line 102**: Invalid Path - `make/just`
- **Line 102**: Invalid Path - `make/g`
- **Line 103**: Invalid Path - `reset/just`
- **Line 103**: Invalid Path - `reset/g`
- **Line 105**: Invalid Path - `up-d/just`
- **Line 105**: Invalid Path - `up-d/g`
- **Line 107**: Invalid Path - `down/just`
- **Line 107**: Invalid Path - `down/g`
- **Line 108**: Invalid Path - `logs/just`
- **Line 108**: Invalid Path - `logs/g`
- **Line 109**: Invalid Path - `ps/just`
- **Line 109**: Invalid Path - `ps/g`
- **Line 110**: Invalid Path - `shell/just`
- **Line 110**: Invalid Path - `shell/g`
- **Line 111**: Invalid Path - `rebuild/just`
- **Line 111**: Invalid Path - `rebuild/g`
- **Line 114**: Invalid Path - `python/just`
- **Line 114**: Invalid Path - `python/g`
- **Line 115**: Invalid Path - `web/just`
- **Line 115**: Invalid Path - `web/g`
- **Line 116**: Invalid Path - `fast/just`
- **Line 116**: Invalid Path - `fast/g`
- **Line 117**: Invalid Path - `test/just`
- **Line 117**: Invalid Path - `test/g`
- **Line 119**: Invalid Path - `lint/just`
- **Line 119**: Invalid Path - `lint/g`
- **Line 120**: Invalid Path - `type-check/just`
- **Line 120**: Invalid Path - `type-check/g`
- **Line 123**: Invalid Path - `add-entity/just`
- **Line 123**: Invalid Path - `add-entity/g`
- **Line 152**: Invalid Path - `docs/documentation-audit-report-fixed.md`
- **Line 161**: Invalid Path - `//api.haven.local/health`
- **Line 150**: Invalid Command - `just database::up`
- **Line 150**: Invalid Command - `just docker::up`
- **Line 150**: Invalid Command - `just testing::all`

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
- **Line 231**: Invalid Path - `//api.haven.local/health`
- **Line 241**: Invalid Path - `//api`
- **Line 241**: Invalid Path - `8080/health`

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

- **Line 81**: Invalid Path - `./.tmp`
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
- **Line 86**: Invalid Path - `//api.haven.local`
- **Line 87**: Invalid Path - `//api.haven.local/health`
- **Line 88**: Invalid Path - `//api.haven.local/docs`
- **Line 89**: Invalid Path - `//api.haven.local/graphql`
- **Line 5**: Invalid Command - `just docker::up               # Start all services`
- **Line 5**: Invalid Command - `just docker::down              # Stop all services`
- **Line 5**: Invalid Command - `just docker::reset             # Full reset (removes data)`
- **Line 5**: Invalid Command - `just docker::shell             # Shell into API container`
- **Line 5**: Invalid Command - `just database::console-docker        # PostgreSQL console`
- **Line 5**: Invalid Command - `just docker::test              # Run tests in container`
- **Line 5**: Invalid Command - `just docker::lint              # Run linting in container`
- **Line 5**: Invalid Command - `just clean-docker                             # Project cleanup`
- **Line 113**: Invalid Command - `just database::up`
- **Line 113**: Invalid Command - `just docker::up`

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
- **Line 117**: Invalid Path - `//api.haven.local/metrics`
- **Line 137**: Invalid Path - `I/O`
- **Line 156**: Invalid Path - `//jaeger`
- **Line 189**: Invalid Path - `/health/live`
- **Line 194**: Invalid Path - `/health/ready`
- **Line 320**: Invalid Path - `//api.haven.local/admin/debug`
- **Line 388**: Invalid Path - `created/updated`
- **Line 431**: Broken Link - [Configuration Reference](configuration.md)
- **Line 432**: Broken Link - [Troubleshooting Guide](troubleshooting.md)

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
- **Line 233**: Invalid Command - `just database::up             # Start PostgreSQL`
- **Line 233**: Invalid Command - `just testing::python       # Run Python tests`
- **Line 233**: Invalid Command - `just type-python       # Python type checking`
- **Line 233**: Invalid Command - `just check-python      # All Python quality gates`
- **Line 233**: Invalid Command - `just testing::web          # Run TypeScript/React tests`
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
- **Line 132**: Invalid Path - `docs.haven.local`
- **Line 35**: Invalid Path - `I/O`
- **Line 66**: Invalid Path - `conf/local`
- **Line 76**: Invalid Path - `query/mutation`
- **Line 97**: Invalid Path - `up/down`
- **Line 133**: Invalid Path - `docs/adr/`
- **Line 149**: Invalid Path - `Authentication/authorization`
- **Line 152**: Invalid Path - `CI/CD`
- **Line 24**: Invalid Command - `just docs`
- **Line 96**: Invalid Command - `just install`
- **Line 97**: Invalid Command - `just database::up`
- **Line 98**: Invalid Command - `just database::migrate`
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
- **Line 42**: Invalid Path - `//api.haven.local`

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
- **Line 18**: Invalid Path - `//api.haven.local/openapi.json`
- **Line 23**: Invalid Path - `apps/web/src/types/domain.ts`
- **Line 33**: Invalid Path - `apps/web/src/services/api/generated`
- **Line 44**: Invalid Path - `//api.haven.local/health`
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

### docs/project-management/tasks/closed/implement-migration-strategy.md

- **Line 42**: Invalid Path - `//haven`
- **Line 42**: Invalid Path - `5432/haven`
- **Line 51**: Invalid Path - `dev/staging/prod`
- **Line 52**: Invalid Path - `CI/CD`
- **Line 58**: Invalid Path - `pros/cons`
- **Line 16**: Invalid Command - `just database::migrate  # Runs from local Python environment`

### docs/project-management/tasks/closed/local-cors-and-domains.md

- **Line 54**: Invalid Path - `haven.local`
- **Line 21**: Invalid Path - `//web.haven.local`
- **Line 22**: Invalid Path - `//localhost`
- **Line 23**: Invalid Path - `//app.haven.local`
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

- **Line 31**: Invalid Path - `//api.haven.local`
- **Line 32**: Invalid Path - `//api.haven.local/graphql`
- **Line 44**: Invalid Path - `migrations/models`
- **Line 65**: Invalid Path - `CI/CD`
- **Line 87**: Invalid Path - `8080/5432`
- **Line 19**: Invalid Command - `just docker::up`
- **Line 19**: Invalid Command - `just database::up                  # Start PostgreSQL`
- **Line 19**: Invalid Command - `just run-api-docker         # Start API with hot-reload`
- **Line 19**: Invalid Command - `just database::migrate-docker`
- **Line 60**: Invalid Command - `just database::make "add_user_table"    # Generate migration`
- **Line 60**: Invalid Command - `just database::migrate                  # Apply migrations`
- **Line 66**: Invalid Command - `just database::migrate-docker           # Apply migrations`
- **Line 66**: Invalid Command - `just database::make-docker "add_field"  # Generate in container`

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
- **Line 17**: Invalid Path - `//api.haven.local/api/v1/ttr/tasks`
- **Line 18**: Invalid Path - `//api.haven.local/docs`
- **Line 21**: Invalid Path - `//api.haven.local/graphql`
- **Line 44**: Invalid Path - `tasks/milestones`
- **Line 113**: Invalid Path - `tests/unit/domain/test_repository.py`
- **Line 113**: Invalid Path - `tests/unit/infrastructure/test_repository_repository.py`
- **Line 113**: Invalid Path - `tests/unit/application/test_repository_service.py`
- **Line 117**: Invalid Path - `venv/bin/activate`
- **Line 141**: Invalid Path - `tests/unit/domain/test_user.py`
- **Line 141**: Invalid Path - `tests/unit/infrastructure/test_user_repository.py`
- **Line 141**: Invalid Path - `tests/unit/application/test_user_service.py`
- **Line 205**: Invalid Path - `docs/roadmap.md`
- **Line 218**: Invalid Path - `//api.haven.local/api/v1/diffs/generate`
- **Line 218**: Invalid Path - `application/json`
- **Line 227**: Invalid Path - `//api.haven.local/api/v1/diffs/status/`
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
- **Line 494**: Invalid Path - `//web.haven.local`
- **Line 501**: Invalid Path - `Create/edit`
- **Line 502**: Invalid Path - `loading/error`
- **Line 576**: Invalid Path - `//haven.local`
- **Line 627**: Invalid Path - `add/remove`
- **Line 636**: Invalid Path - `just/help.sh`
- **Line 661**: Invalid Path - `just/common.just`
- **Line 12**: Invalid Command - `just docker::up-d`
- **Line 170**: Invalid Command - `just database::up       # Start PostgreSQL`
- **Line 170**: Invalid Command - `just check-python # Python lint + type + test (was missing)`
- **Line 170**: Invalid Command - `just check-web   # Web lint + type + test (was missing)`
- **Line 245**: Invalid Command - `just demos::docker`
- **Line 245**: Invalid Command - `just docker::up-d`
- **Line 245**: Invalid Command - `just demos::health`
- **Line 245**: Invalid Command - `just docker::test`
- **Line 245**: Invalid Command - `just database::console-docker`
- **Line 276**: Invalid Command - `just testing::coverage`
- **Line 276**: Invalid Command - `just demos::api`
- **Line 276**: Invalid Command - `just demos::graphql`
- **Line 307**: Invalid Command - `just docker::up`
- **Line 307**: Invalid Command - `just docker::logs api | grep -i reload`
- **Line 334**: Invalid Command - `just demos::migrations`
- **Line 334**: Invalid Command - `just database::current-docker`
- **Line 334**: Invalid Command - `just database::migrate-run`
- **Line 334**: Invalid Command - `just --list | grep db-.*-docker`
- **Line 364**: Invalid Command - `just docker::reset`
- **Line 392**: Invalid Command - `just database::migrate`
- **Line 420**: Invalid Command - `just demos::health      # Health endpoints`
- **Line 420**: Invalid Command - `just demos::api         # REST CRUD operations`
- **Line 420**: Invalid Command - `just demos::graphql     # GraphQL queries`
- **Line 420**: Invalid Command - `just demos::docker      # Container status`
- **Line 420**: Invalid Command - `just demos::migrations  # Migration strategies`
- **Line 420**: Invalid Command - `just demos::all`
- **Line 447**: Invalid Command - `just demos::cors`
- **Line 489**: Invalid Command - `just docker::up-d`
- **Line 518**: Invalid Command - `just demos::sync`
- **Line 526**: Invalid Command - `just docker::up-d`
- **Line 526**: Invalid Command - `just check-api-compat`
- **Line 556**: Invalid Command - `just demos::https`
- **Line 638**: Invalid Command - `just --list         # All commands`
- **Line 638**: Invalid Command - `just docker::help   # Module help`
- **Line 638**: Invalid Command - `just testing::all   # Module commands`
- **Line 646**: Invalid Command - `just database::up        # Start PostgreSQL`
- **Line 646**: Invalid Command - `just docker::logs api    # View API logs`
- **Line 646**: Invalid Command - `just testing::python     # Run Python tests`
- **Line 646**: Invalid Command - `just demos::all          # Run all demos`
- **Line 646**: Invalid Command - `just database::up              # Shows deprecation warning`
- **Line 646**: Invalid Command - `just docker::up         # Shows deprecation warning`
- **Line 10**: Invalid Command - `just docker::test`
- **Line 168**: Invalid Command - `just --list`
- **Line 243**: Invalid Command - `just docker::test`
- **Line 269**: Invalid Command - `just database::migrate-docker`
- **Line 299**: Invalid Command - `just demo-diff-generation`
- **Line 300**: Invalid Command - `just demo-diff-generation`
- **Line 305**: Invalid Command - `just docker::up`
- **Line 332**: Invalid Command - `just database::current-docker`
- **Line 332**: Invalid Command - `just database::migrate-run`
- **Line 390**: Invalid Command - `just --list`
- **Line 390**: Invalid Command - `just docker::up`
- **Line 418**: Invalid Command - `just demos::all`
- **Line 445**: Invalid Command - `just demos::cors`

### docs/quickstart.md

- **Line 9**: Invalid Path - `//github.com/casey/just`
- **Line 16**: Invalid Path - `//github.com/jazzydog-labs/haven.git`
- **Line 43**: Invalid Path - `venv/bin/activate`
- **Line 60**: Invalid Path - `//api.haven.local`
- **Line 64**: Invalid Path - `//api.haven.local/health`
- **Line 71**: Invalid Path - `//api.haven.local/docs`
- **Line 75**: Invalid Path - `//api.haven.local/graphql`
- **Line 83**: Invalid Path - `//api.haven.local/api/v1/records`
- **Line 84**: Invalid Path - `application/json`
- **Line 141**: Invalid Path - `//api.haven.local/api/v1/records/`
- **Line 206**: Invalid Path - `//github.com/jazzydog-labs/haven/issues`
- **Line 24**: Invalid Command - `just database::up`
- **Line 24**: Invalid Command - `just database::migrate`
- **Line 161**: Invalid Command - `just --list`
- **Line 177**: Broken Link - [Architecture Overview](architecture.md)
- **Line 179**: Broken Link - [Development Environment](local-setup.md)
- **Line 180**: Broken Link - [Testing](testing.md)
- **Line 180**: Broken Link - [Code Quality](quality.md)

### docs/workflow/frontend-backend-sync.md

- **Line 62**: Invalid Path - `apps/web/src/types/openapi.prev.json`
- **Line 15**: Invalid Path - `request/response`
- **Line 81**: Invalid Path - `githooks/pre-commit`
- **Line 82**: Invalid Path - `domain/entities`
- **Line 87**: Invalid Path - `CI/CD`
- **Line 139**: Invalid Path - `hey-api/openapi-ts`
- **Line 140**: Invalid Path - `//api.haven.local/openapi.json`
- **Line 141**: Invalid Path - `apps/web/src/services/api/generated`
- **Line 19**: Invalid Command - `just docker::up-d`
- **Line 19**: Invalid Command - `just check-api-compat`
- **Line 113**: Invalid Command - `just docker::up-d`

### docs/workflow/normalize-docs.md

- **Line 216**: Invalid Path - `scripts/fix-common-docs.sh`
- **Line 217**: Invalid Path - `tests/test_documentation.py`
- **Line 89**: Invalid Path - `*.md`
- **Line 89**: Invalid Path - `s/just`
- **Line 89**: Invalid Path - `up/just`
- **Line 89**: Invalid Path - `up/g`
- **Line 93**: Invalid Path - `//web.haven.local`
- **Line 94**: Invalid Path - `//api.haven.local`
- **Line 108**: Invalid Path - `docs/documentation-audit-report-fixed.md`
- **Line 110**: Invalid Path - `before/after`
- **Line 120**: Invalid Path - `compile/run`
- **Line 155**: Invalid Path - `//api.haven.local/docs`
- **Line 162**: Invalid Path - `src/haven/`
- **Line 186**: Invalid Path - `github/workflows/docs.yml`
- **Line 193**: Invalid Path - `actions/checkout`
- **Line 47**: Invalid Command - `just database::up`
- **Line 47**: Invalid Command - `just database::up`
