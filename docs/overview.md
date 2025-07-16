# Haven — Documentation Navigation Hub

*Your complete guide to the Haven codebase and development workflow*

---

## 🎯 Quick Start Paths

**New to Haven?** → [`docs/project-management/spec.md`](#project-specification) → [`CLAUDE.md`](#development-workflow)  
**Setting up locally?** → [`docs/development/local-setup.md`](#environment-setup) → [`just bootstrap`](#task-runner)  
**Adding a feature?** → [`docs/architecture/architecture.md`](#clean-architecture-guide) → [`docs/api/`](#api-references)  
**Making changes?** → [`docs/development/definition-of-done.md`](#quality-checklist) → [`docs/project-management/work-log.md`](#development-tracking)

---

## 📚 Core Documentation

### 🎯 Project Specification
- **[`docs/project-management/spec.md`](project-management/spec.md)** `#requirements #goals #success-criteria`
  - Project requirements and success criteria
  - Technology choices and constraints
  - **When to read**: Understanding project purpose and scope

### 🏗️ Clean Architecture Guide  
- **[`docs/architecture/architecture.md`](architecture/architecture.md)** `#patterns #layers #design`
  - Clean Architecture implementation patterns
  - Layer responsibilities and dependencies
  - Sequence flows and design decisions
  - **When to read**: Before implementing features or refactoring

### 📋 Development Tracking
- **[`docs/project-management/work-log.md`](project-management/work-log.md)** `#completed #achievements #history`
  - Comprehensive log of completed development work
  - Phase summaries and technical achievements
  - **When to read**: Understanding what's been built

- **[`docs/project-management/todo.md`](project-management/todo.md)** `#current #tasks #immediate`
  - Current tasks and immediate next steps
  - Command testing checklist
  - **When to read**: Daily development planning

- **[`docs/project-management/roadmap.md`](project-management/roadmap.md)** `#planning #features #debt`
  - Feature planning and technical debt tracking
  - Sprint goals and long-term vision
  - **When to read**: Sprint planning and prioritization

- **[`docs/project-management/commits-plan.md`](project-management/commits-plan.md)** `#implementation #milestones #progress`
  - Implementation milestones and progress tracking
  - Original plan vs actual achievements
  - **When to read**: Understanding implementation history

---

## ⚙️ Development Workflow

### 🚀 Development Workflow
- **[`CLAUDE.md`](../CLAUDE.md)** `#workflow #commands #daily`
  - Fast development operations and daily commands
  - Quick start guide and task runner reference
  - **When to read**: Daily development workflow

### ✅ Quality Checklist
- **[`docs/development/definition-of-done.md`](development/definition-of-done.md)** `#quality #checklist #standards`
  - Complete quality checklist for task completion
  - Testing, linting, documentation requirements
  - **When to read**: Before committing any changes

### 🛠️ Environment Setup
- **[`docs/development/local-setup.md`](development/local-setup.md)** `#setup #environment #prerequisites`
  - Local development environment setup
  - Prerequisites and installation guide
  - **When to read**: First-time setup or troubleshooting

---

## 🧪 Development Guides

### 🧪 Testing Strategy
- **[`docs/development/testing.md`](development/testing.md)** `#testing #fixtures #coverage`
  - Test strategy, patterns, and coverage requirements
  - Pytest configuration and fixture usage
  - **When to read**: Writing tests or debugging test issues

### 🔍 Code Quality
- **[`docs/development/quality.md`](development/quality.md)** `#linting #typing #standards`
  - Linting, type checking, and code standards
  - Ruff and Pyright configuration details
  - **When to read**: Setting up quality tools or resolving lint errors

### 🔧 Configuration Management
- **[`docs/development/configuration.md`](development/configuration.md)** `#hydra #config #environments`
  - Hydra configuration management and usage
  - Multi-environment setup and overrides
  - **When to read**: Adding configuration or environment support

### 🗃️ Database Operations
- **[`docs/development/alembic.md`](development/alembic.md)** `#database #migrations #schema`
  - Database migration workflows and procedures
  - Alembic usage and best practices
  - **When to read**: Making database schema changes

### 🔄 Safe Refactoring
- **[`docs/development/refactoring.md`](development/refactoring.md)** `#refactoring #safety #procedures`
  - Safe code reorganization procedures
  - Directory restructuring and config migrations
  - **When to read**: Planning code reorganization or cleanup

---

## 🌐 API References

### 🔌 REST API
- **[`docs/api/rest.md`](api/rest.md)** `#rest #endpoints #examples`
  - REST endpoint reference with examples
  - Request/response schemas and error codes
  - **When to read**: Implementing or consuming REST endpoints

### 📡 GraphQL API  
- **[`docs/api/graphql.md`](api/graphql.md)** `#graphql #schema #queries`
  - GraphQL schema and query examples
  - Mutations, subscriptions, and pagination
  - **When to read**: Working with GraphQL features

---

## 🐳 Operations

### 🐳 Container Deployment
- **[`docs/operations/docker.md`](operations/docker.md)** `#docker #containers #security`
  - Container build and security practices
  - Multi-stage Dockerfile and hardening
  - **When to read**: Deploying or optimizing containers

### 🖥️ Command Line Interface
- **[`docs/operations/cli.md`](operations/cli.md)** `#cli #commands #diff-generation`
  - Haven CLI tool for git diff generation
  - Command reference and usage examples
  - **When to read**: Using Haven as a command-line tool

---

## 🏗️ Architecture Overview

### Monorepo Structure
```
haven/
├── apps/
│   ├── api/          # Python backend (FastAPI + GraphQL)
│   └── web/          # React frontend (TypeScript + Vite)
├── packages/         # Shared libraries (future SDK)
├── docs/            # Documentation (MkDocs)
├── scripts/         # Build and utility scripts (demo-commits.sh, demo-diff-generation.sh)
└── tools/           # Development tooling
```

### Technology Stack
- **Backend**: FastAPI + Strawberry GraphQL + SQLAlchemy 2.x
- **Frontend**: React + TypeScript + Vite + Tailwind CSS
- **Database**: PostgreSQL with Alembic migrations  
- **Quality**: Ruff + Pyright + pytest + ESLint + Prettier
- **Config**: Hydra for multi-environment configuration
- **Containers**: Docker with Chainguard security-hardened images

---

## 🔍 Finding What You Need

### By Task Type

**🏗️ Building Features**
- Architecture patterns → [`docs/architecture.md`](architecture.md)
- API design → [`docs/api/`](api/)
- Database changes → [`docs/alembic.md`](alembic.md)
- Quality gates → [`docs/definition-of-done.md`](definition-of-done.md)

**🐛 Debugging Issues**
- Environment setup → [`docs/local-setup.md`](local-setup.md)
- Test failures → [`docs/testing.md`](testing.md)
- Lint errors → [`docs/quality.md`](quality.md)
- Configuration → [`docs/configuration.md`](configuration.md)

**🔄 Maintaining Code**
- Refactoring safely → [`docs/refactoring.md`](refactoring.md)
- Understanding history → [`work-log.md`](../work-log.md)
- Planning work → [`docs/roadmap.md`](roadmap.md)
- Current tasks → [`todo.md`](../todo.md)

**📖 Learning the System**
- Project overview → [`docs/spec.md`](spec.md)
- Architecture design → [`docs/architecture.md`](architecture.md)
- Development workflow → [`CLAUDE.md`](../CLAUDE.md)
- Implementation story → [`docs/commits-plan.md`](commits-plan.md)

### By File Tags

Use these tags to quickly find relevant documentation:

- `#requirements #goals` → Project specification and success criteria
- `#patterns #layers #design` → Architecture and design patterns
- `#workflow #commands #daily` → Development workflow and commands
- `#quality #checklist #standards` → Quality gates and standards
- `#testing #fixtures #coverage` → Testing strategy and patterns
- `#setup #environment #prerequisites` → Environment setup
- `#config #hydra #environments` → Configuration management
- `#database #migrations #schema` → Database operations
- `#rest #graphql #api` → API documentation
- `#docker #containers #security` → Container and deployment
- `#cli #commands #diff-generation` → Command-line interface and tools
- `#scripts #automation #demos` → Build scripts and demo automation
- `#planning #features #debt` → Project planning and roadmap
- `#completed #achievements #history` → Completed work tracking
- `#current #tasks #immediate` → Current development tasks

---

## 📱 Quick Reference Commands

```bash
# Setup and run
just bootstrap          # Complete environment setup
just db-up             # Start PostgreSQL
just run               # Start API server with hot reload

# Development workflow  
just test-python       # Run Python tests
just lint-python       # Check Python code quality
just type-python       # Python type checking
just check-python      # All Python quality gates

just test-web          # Run TypeScript/React tests
just lint-web          # Check TypeScript code quality
just check-web         # All TypeScript quality gates

# Utilities
just docs              # Build documentation
just demo-commits      # Demo git diff viewer (auto-starts server)
just demo-diff-generation  # Demo git diff API (requires server)
just clean             # Clean environment
just --list            # Show all available commands

# CLI tools (integrated with diff2html)
just cli-list-commits          # List commits via Just command
just cli-generate             # Generate HTML diffs via Just command  
just cli-generate-to /path    # Generate diffs to specific directory

haven-cli list-commits        # Direct CLI - List commits for diff generation
haven-cli generate --verbose  # Direct CLI - Generate HTML diff files with progress

# Direct script access
./scripts/demo-commits.sh apps/api .venv/bin/python  # Run demo script directly
```

---

**💡 Pro Tip**: Bookmark this page and use the file tags to quickly navigate to the documentation you need. Each document is designed to be self-contained while linking to related resources.

*This overview is your starting point for navigating the Haven documentation ecosystem. Keep it updated as the project evolves!*