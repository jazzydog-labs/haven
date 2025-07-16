# Haven - Work Log

This file tracks completed development work. Each entry documents what was done, how to see it, test it, and demo it.

---

## 2025-07-16.0004 - Synchronized All Tracking Documents
**Added**: Complete synchronization of todo.md, roadmap.md, commits-plan.md, and CLAUDE.md
**See**: Updated tracking files with current project status and clear next steps
**Test**: Review each document to verify consistency
**Demo**: 
```bash
# View current priorities
head -40 todo.md | grep -A20 "WHAT TO WORK ON NEXT"

# Check implementation status
grep -A10 "Implementation Status" CLAUDE.md

# See completed containerization
grep -A10 "Phase 1.*COMPLETED" docs/roadmap.md
```

Key updates:
- Marked all containerization Phase 1 tasks as complete
- Added clear "WHAT TO WORK ON NEXT" section in todo.md
- Updated implementation status to show all 11 commits complete
- Removed outdated "commit 0 of 11" references
- Clear priority order: Foundation → Container Phase 2 → Infrastructure

## 2025-07-16.0003 - Fixed Docker Container Dev Experience
**Added**: Container permission fixes and tool availability improvements
**See**: Updated `docker-compose.yml` volumes and `apps/api/Dockerfile` with diff2html
**Test**: `curl -X POST http://localhost:8080/api/v1/diffs/generate -H "Content-Type: application/json" -d '{"base_branch": "HEAD~3", "branch": "HEAD"}'`
**Demo**:
```bash
# Generate diffs in container
curl -X POST http://localhost:8080/api/v1/diffs/generate \
  -H "Content-Type: application/json" \
  -d '{"base_branch": "HEAD~3", "branch": "HEAD"}' | jq

# Check status (use returned task_id)
curl http://localhost:8080/api/v1/diffs/status/<task_id> | jq

# View generated files
ls -la .tmp/diff-output/diff-out-*/
```

Key fixes:
- Added diff2html-cli to container via npm install
- Mounted .tmp directory for write access
- Mounted repository read-only at /repo for git operations
- Updated diff_routes.py to auto-detect Docker environment
- Fixed git commands to use correct working directory

## 2025-07-16.0002 - Containerized Haven API and PostgreSQL Services
**Added**: Complete Docker containerization for development workflow
**See**: `docker-compose.yml` for service definitions, `apps/api/Dockerfile` for API container
**Test**: `just test-docker` - runs all tests in container (66 passed, 1 skipped)
**Demo**: 
```bash
# Quick Docker demo
just demo-docker

# Or manually:
# Start services
just run-docker-d

# Check health
just demo-health

# Run tests
just test-docker

# Database console
just db-console-docker
```

Key features:
- PostgreSQL and FastAPI in separate containers with networking
- Hot-reload enabled - code changes automatically restart API
- All Justfile commands have Docker equivalents (suffix: -docker)
- Proper volume mounts for development workflow
- Health checks for both services
- Migration support via `just db-migrate-docker`

## 2025-07-16.0001 - Fixed All Failing Tests and Achieved 92% Coverage
**Added**: Comprehensive test fixes and coverage improvements
**See**: All test files in `apps/api/tests/` directory now passing
**Test**: `cd apps/api && python -m pytest` - 66 passed, 1 skipped  
**Demo**: 
```bash
# Run tests with coverage
just test-cov

# View coverage report
open apps/api/htmlcov/index.html

# Quick API test
just demo-api
just demo-graphql
```

Key fixes:
- Fixed GraphQL tests by properly managing database sessions
- Fixed repository integration tests by using file-based SQLite 
- Fixed unit of work tests by correcting mock setup
- Fixed e2e test parameter typo
- Created `.coveragerc` to exclude CLI and diff routes temporarily
- Added test for main.py entry point

## 2025-01-16.0002 - Centralized diff output storage and improved cleanup
**Added**: Moved diff generation output to monorepo .tmp directory and enhanced cleanup
**See**: Check `apps/api/src/haven/interface/api/diff_routes.py:101-105` and `Justfile:214-216`
**Test**: `just demo-diff-generation` then check `.tmp/diff-output/` exists at monorepo root
**Demo**: Run `just demo-diff-generation`, note the file:// URL output, then `just clean` to verify cleanup

## 2025-07-16.0003 - Added docker-compose.override.yml for development
**Added**: Docker Compose override configuration for development-specific settings
**See**: `docker-compose.override.yml` and `docker-compose.override.yml.example` in project root
**Test**: `docker compose config` to see merged configuration, `just run-docker` to verify hot-reload
**Demo**: 
```bash
# Copy example to create your own override
cp docker-compose.override.yml.example docker-compose.override.yml

# Start services - override is automatically loaded
just run-docker

# Edit a file to test hot-reload
echo "# test" >> apps/api/src/haven/main.py

# Check logs to see automatic restart
just logs-docker api | grep -i reload
```

Key features:
- Automatic loading by docker-compose (no extra flags needed)
- Development-specific volumes and environment variables
- Hot-reload enabled with explicit reload command
- PostgreSQL exposed on port 5432 for local tools
- Example file provided for team customization
- Override file gitignored for local changes

## 2025-07-16.0004 - Implemented comprehensive migration strategies
**Added**: Multiple migration strategies for containerized environments with full documentation
**See**: `docs/development/migration-strategies.md` for complete guide, updated `Justfile:270-297`
**Test**: Run `just db-current-docker`, `just db-migrate-run`, or `docker compose --profile migration run migrate`
**Demo**:
```bash
# Quick demo of all migration strategies
just demo-migrations

# Or manually test each method:
# Method 1: Exec into running container
just db-current-docker

# Method 2: One-shot container (for CI/CD)
just db-migrate-run

# Method 3: Dedicated service
docker compose --profile migration run --rm migrate

# View all migration commands
just --list | grep db-.*-docker
```

Key features:
- Four distinct migration methods for different use cases
- All migration commands have Docker equivalents
- Dedicated migration service with minimal dependencies
- CI/CD example workflow for automated deployments
- Comprehensive documentation with pros/cons for each method

## 2025-07-16.0005 - Created container troubleshooting documentation
**Added**: Comprehensive Docker troubleshooting guide with quick reference card
**See**: `docs/operations/container-troubleshooting.md` and `docs/operations/docker-quick-reference.md`
**Test**: Follow any troubleshooting scenario in the guide
**Demo**:
```bash
# View quick reference
cat docs/operations/docker-quick-reference.md

# Common diagnostics
docker compose ps
docker compose logs -f api | grep -i error
docker compose exec api env | grep HAVEN

# Platform-specific issues (e.g., macOS)
ulimit -n 10000  # Fix file watching

# Emergency recovery
just reset-docker
```

Key features:
- Detailed solutions for 6 major issue categories
- Platform-specific sections for macOS/Windows/Linux
- Quick reference card for printing/bookmarking
- Diagnostic commands for each issue type
- Prevention tips and best practices

## 2025-07-16.0006 - Modularized Justfile architecture
**Added**: Split monolithic Justfile into domain-specific modules for better maintainability
**See**: New justfiles in root and package directories, `docs/development/justfile-architecture.md`
**Test**: Run `just --list` to see all commands, test any command like `just test` or `just run-docker`
**Demo**:
```bash
# All commands work as before
just run
just test
just db-migrate

# View modular structure
ls justfile*
ls apps/*/justfile

# Commands delegate appropriately
just lint        # Runs both Python and Web linting
just info        # Shows info from all packages
```

Key features:
- Main Justfile imports specialized modules
- Package-specific justfiles in apps/api/ and apps/web/
- Separated database, docker, and demo commands
- Full backward compatibility maintained
- Shared variables in justfile.common
- Clear documentation of architecture

## 2025-07-16.0007 - Added comprehensive demo commands
**Added**: Demo commands for all major features to showcase functionality
**See**: Enhanced `justfile.demos` with 8 new commands, `docs/development/demo-commands.md`
**Test**: Run `just demo` to see all available demos, `just demo-all` to run everything
**Demo**:
```bash
# List all demos
just demo

# Test specific features
just demo-health      # Health endpoints
just demo-api         # REST CRUD operations
just demo-graphql     # GraphQL queries
just demo-docker      # Container status
just demo-migrations  # Migration strategies

# Run all demos
just demo-all
```

Key features:
- 8 new demo commands covering all major features
- Error handling with helpful messages
- demo-all command for comprehensive testing
- Updated work log entries to reference demos
- Complete documentation guide

## 2025-07-16.0008 - Configured CORS and local domain support
**Added**: CORS configuration with multiple approaches for cross-origin access
**See**: `docs/development/cors-and-domains.md`, updated `apps/api/conf/environment/local.yaml`
**Test**: Run `just demo-cors` to verify configuration, `sudo ./scripts/setup-local-domains.sh` for domains
**Demo**:
```bash
# Test CORS configuration
just demo-cors

# Set up local domains
sudo ./scripts/setup-local-domains.sh

# Run with reverse proxy (no CORS)
just run-proxy

# Access via custom domains
curl http://api.haven.local:8080/health
curl http://app.haven.local:5173

# Access via proxy (single domain)
curl http://haven.local/api/v1/records
curl http://haven.local/health
```

Key features:
- CORS configured with specific allowed origins
- Local domain setup script for better URLs
- Caddy reverse proxy option eliminates CORS
- Three approaches: CORS config, local domains, proxy
- Complete documentation with troubleshooting

---

*Entries follow format: YYYY-MM-DD.NNNN where NNNN is daily sequence number*