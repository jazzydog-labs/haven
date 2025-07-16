# Justfile Architecture

The Haven project uses a modular Justfile architecture to organize build commands and development workflows.

## Structure Overview

```
Justfile                # Main orchestrator, imports all modules
justfile.common         # Shared variables and settings
justfile.database       # Database-specific commands
justfile.docker         # Docker and container commands
justfile.demos          # Demo and showcase commands
apps/api/justfile       # API-specific commands
apps/web/justfile       # Web-specific commands
```

## Module Responsibilities

### Main Justfile
- Overall orchestration and coordination
- Bootstrap commands for the entire monorepo
- Cross-package commands that span API and web
- Import and delegation to specialized modules

### justfile.common
- Shared variable definitions (api_dir, web_dir, python, pip)
- Common settings used across all modules
- Export declarations for cross-module usage

### justfile.database
- All database-related commands
- PostgreSQL management (start, stop, reset)
- Migration commands (create, run, history, rollback)
- Database console access

### justfile.docker
- Docker Compose commands
- Container management (build, run, stop)
- Docker-specific testing and quality checks
- Container utilities (shell, logs, cleanup)

### justfile.demos
- Feature demonstration commands
- Showcase utilities for stakeholders
- Demo-specific workflows

### apps/api/justfile
- Python-specific commands
- API server management
- Python testing, linting, and formatting
- Virtual environment management

### apps/web/justfile
- Node.js/TypeScript commands
- Web development server
- Frontend build and testing
- NPM dependency management

## Command Organization

Commands are organized by their primary function:

1. **Development**: run, shell, logs
2. **Quality**: lint, type, test, check
3. **Database**: db-*, migrations
4. **Docker**: *-docker variants, container utilities
5. **Build**: build, ci, docs
6. **Utilities**: clean, info, demo

## Backward Compatibility

All existing commands from the monolithic Justfile are preserved:
- Main commands delegate to package-specific justfiles
- Docker commands remain at the root level
- Database commands are globally accessible
- No breaking changes for existing workflows

## Usage Patterns

### Running Commands
```bash
# Root-level commands work as before
just run
just test
just db-migrate

# Package-specific commands via delegation
just run-api      # Delegates to apps/api/justfile
just test-python  # Delegates to apps/api/justfile

# Direct package commands (from package directory)
cd apps/api && just test
cd apps/web && just build
```

### Variable Scoping
Variables defined in `justfile.common` are available to all imported modules:
- `api_dir`: Path to API package
- `web_dir`: Path to web package  
- `python`: Python interpreter path
- `pip`: Pip command path

### Adding New Commands
1. Determine the appropriate module for the command
2. Add the command to the relevant justfile
3. If needed, add a delegating command to the main Justfile
4. Update documentation

## Benefits

1. **Maintainability**: Commands are organized by domain
2. **Scalability**: Easy to add new packages with their own justfiles
3. **Clarity**: Clear separation of concerns
4. **Flexibility**: Packages can be developed independently
5. **Reusability**: Common patterns extracted to shared modules

## Future Enhancements

- Add justfile for documentation commands
- Create justfile for deployment/release commands
- Support for additional packages (SDK, CLI tools)
- Integration with CI/CD pipelines
- Package-specific variable overrides