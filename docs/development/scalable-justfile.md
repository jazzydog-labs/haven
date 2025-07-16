# Scalable Justfile System for Monorepo

## Overview

This system provides a hierarchical, discoverable, and maintainable command structure for large monorepos with multiple languages and services.

## Directory Structure

```
monorepo/
├── justfile                 # Main entry point
├── .just/                   # Just-related utilities
│   ├── common.just         # Shared recipes/variables
│   ├── help.sh            # Help formatting script
│   └── completions.sh     # Shell completions
├── packages/
│   ├── api-gateway/
│   │   ├── justfile       # Local commands
│   │   └── ...
│   ├── auth-service/
│   │   ├── justfile
│   │   └── ...
│   └── web-app/
│       ├── justfile
│       └── ...
└── tools/
    ├── docker.just
    ├── testing.just
    └── deploy.just
```

## Main Justfile (Root)

```just
# Main justfile - Entry point for all commands
set dotenv-load := true
set export := true

# Import common utilities
import '.just/common.just'

# Import tool-specific commands
mod docker 'tools/docker.just'
mod test 'tools/testing.just'
mod deploy 'tools/deploy.just'

# Import package-specific commands
mod api 'packages/api-gateway/justfile'
mod auth 'packages/auth-service/justfile'
mod web 'packages/web-app/justfile'

# Default command - shows interactive menu
default:
    @just --choose

# Show hierarchical help menu
help:
    @bash .just/help.sh

# Alias for help
h: help

# List all available commands with descriptions
list-all:
    @echo "🚀 Monorepo Commands"
    @echo "==================="
    @just --list --list-heading ''
    @echo ""
    @echo "📦 Package Commands"
    @echo "==================="
    @echo "  api::     - API Gateway commands (just api::help)"
    @echo "  auth::    - Auth Service commands (just auth::help)"
    @echo "  web::     - Web App commands (just web::help)"
    @echo ""
    @echo "🛠️  Tool Commands"
    @echo "================"
    @echo "  docker::  - Docker commands (just docker::help)"
    @echo "  test::    - Testing commands (just test::help)"
    @echo "  deploy::  - Deployment commands (just deploy::help)"

# Alias for list-all
la: list-all

# Quick navigation commands
@cd PATH:
    echo "Run commands in {{PATH}}:"
    echo "  cd {{PATH}} && just --list"

# Run command in specific package
@in PACKAGE CMD *ARGS:
    cd packages/{{PACKAGE}} && just {{CMD}} {{ARGS}}

# Setup development environment
setup:
    @echo "🔧 Setting up development environment..."
    @just docker::setup
    @just api::install
    @just auth::install
    @just web::install
    @echo "✅ Setup complete!"

# Common development workflow shortcuts
dev: (docker::up) (watch)

# Watch all services for changes
watch:
    #!/usr/bin/env bash
    tmux new-session -d -s dev 'just api::dev'
    tmux split-window -h 'just auth::dev'
    tmux split-window -v 'just web::dev'
    tmux attach-session -t dev

# Run all tests
test-all: test::unit test::integration test::e2e

# Global clean command
clean:
    @echo "🧹 Cleaning all packages..."
    @just api::clean
    @just auth::clean
    @just web::clean
    @just docker::clean
```

## Common Utilities (.just/common.just)

```just
# Common variables and utilities shared across all justfiles

# Colors for output
export RED := '\033[0;31m'
export GREEN := '\033[0;32m'
export YELLOW := '\033[1;33m'
export NC := '\033[0m' # No Color

# Common paths
export MONOREPO_ROOT := justfile_directory()
export PACKAGES_DIR := MONOREPO_ROOT / "packages"
export TOOLS_DIR := MONOREPO_ROOT / "tools"

# Check if command exists
_has CMD:
    @command -v {{CMD}} > /dev/null 2>&1 || (echo "❌ {{CMD}} is required but not installed" && exit 1)

# Formatted output helpers
_info MSG:
    @echo -e "${GREEN}ℹ${NC}  {{MSG}}"

_warn MSG:
    @echo -e "${YELLOW}⚠${NC}  {{MSG}}"

_error MSG:
    @echo -e "${RED}✖${NC}  {{MSG}}"

# Confirm dangerous operations
_confirm MSG:
    @echo -n "{{MSG}} [y/N] " && read ans && [ $${ans:-N} = y ]
```

## Help Formatting Script (.just/help.sh)

```bash
#!/usr/bin/env bash
# Beautiful help menu with categorized commands

cat << 'EOF'
╔══════════════════════════════════════════════════════════════╗
║                    🚀 MONOREPO COMMANDS                      ║
╚══════════════════════════════════════════════════════════════╝

📁 NAVIGATION
  just help              Show this help menu
  just list-all          List all available commands
  just cd <path>         Show commands for specific directory
  just in <pkg> <cmd>    Run command in specific package

🏗️  SETUP & BUILD
  just setup             Setup entire development environment
  just build             Build all packages
  just clean             Clean all build artifacts

🚀 DEVELOPMENT
  just dev               Start all services in development mode
  just watch             Watch all services (opens tmux)
  just logs              Show logs from all services

📦 PACKAGES                    Try: just <package>::help
  api::    API Gateway          • Node.js/Express
  auth::   Auth Service         • Python/FastAPI  
  web::    Web Application      • React/TypeScript

🛠️  TOOLS                       Try: just <tool>::help
  docker:: Container management • build, up, down, logs
  test::   Testing suite        • unit, integration, e2e
  deploy:: Deployment          • staging, production

💡 TIPS
  • Use TAB completion: source .just/completions.sh
  • Quick test: just test-all
  • Package-specific: just api::test
  • Interactive mode: just --choose

Need more? Try 'just list-all' or 'just <module>::help'
EOF
```

## Package-Specific Justfile Example (packages/api-gateway/justfile)

```just
# API Gateway Commands
set dotenv-load := true

# Import common utilities
import '../../.just/common.just'

# Show help for this package
help:
    @echo "📦 API Gateway Commands"
    @echo "======================"
    @just --list --justfile {{justfile()}}

# Install dependencies
install: (_has "node") (_has "npm")
    @_info "Installing API Gateway dependencies..."
    npm ci

# Start development server
dev: install
    @_info "Starting API Gateway in development mode..."
    npm run dev

# Run tests
test: (_has "npm")
    npm test

# Run specific test file
test-file FILE:
    npm test -- {{FILE}}

# Build for production
build: install
    @_info "Building API Gateway..."
    npm run build

# Clean build artifacts
clean:
    @_info "Cleaning API Gateway..."
    rm -rf node_modules dist coverage

# Lint code
lint:
    npm run lint

# Format code
format:
    npm run format

# Check types
typecheck:
    npm run typecheck

# Run all checks (used in CI)
check: lint typecheck test
```

## Tool-Specific Justfile Example (tools/docker.just)

```just
# Docker-related commands

# Import common utilities  
import '../.just/common.just'

# Docker compose file
compose_file := MONOREPO_ROOT / "docker-compose.yml"

# Show help
help:
    @echo "🐳 Docker Commands"
    @echo "=================="
    @just --list --justfile {{justfile()}}

# Setup Docker environment
setup: (_has "docker") (_has "docker-compose")
    @_info "Setting up Docker environment..."
    docker-compose -f {{compose_file}} build

# Start all services
up:
    @_info "Starting all services..."
    docker-compose -f {{compose_file}} up -d

# Stop all services
down:
    @_info "Stopping all services..."
    docker-compose -f {{compose_file}} down

# Show logs
logs SERVICE="":
    #!/usr/bin/env bash
    if [ -z "{{SERVICE}}" ]; then
        docker-compose -f {{compose_file}} logs -f
    else
        docker-compose -f {{compose_file}} logs -f {{SERVICE}}
    fi

# Restart service
restart SERVICE:
    docker-compose -f {{compose_file}} restart {{SERVICE}}

# Execute command in container
exec SERVICE CMD:
    docker-compose -f {{compose_file}} exec {{SERVICE}} {{CMD}}

# Remove all containers and volumes
clean: (_confirm "Remove all Docker containers and volumes?")
    docker-compose -f {{compose_file}} down -v
    docker system prune -f
```

## Shell Completions (.just/completions.sh)

```bash
#!/usr/bin/env bash
# Add to your .bashrc or .zshrc: source /path/to/.just/completions.sh

# Bash completion for just
if [ -n "$BASH_VERSION" ]; then
    _just_completions() {
        local cur prev words cword
        _init_completion || return

        if [[ ${cur} == *::* ]]; then
            # Complete module commands
            local module="${cur%%::*}"
            local cmd="${cur#*::}"
            COMPREPLY=( $(cd "${COMP_WORDS[0]%/*}" && just --list --justfile . 2>/dev/null | grep "^${module}::" | sed "s/^${module}:://") )
        else
            # Complete top-level commands and modules
            COMPREPLY=( $(compgen -W "$(just --list 2>/dev/null | tail -n +2 | awk '{print $1}') api:: auth:: web:: docker:: test:: deploy::" -- "${cur}") )
        fi
    }
    complete -F _just_completions just
fi

# Zsh completion
if [ -n "$ZSH_VERSION" ]; then
    _just() {
        local -a commands modules
        commands=(${(f)"$(just --list 2>/dev/null | tail -n +2 | awk '{print $1}')"})
        modules=(api:: auth:: web:: docker:: test:: deploy::)
        _alternative \
            'commands:command:compadd -a commands' \
            'modules:module:compadd -a modules'
    }
    compdef _just just
fi
```

## Additional Features

### 1. Package Discovery Script

Create `.just/discover-packages.sh`:

```bash
#!/usr/bin/env bash
# Auto-discover packages with justfiles

find packages -name "justfile" -type f | while read -r justfile; do
    dir=$(dirname "$justfile")
    name=$(basename "$dir" | tr '-' '_')
    echo "mod $name '$justfile'"
done
```

### 2. CI/CD Integration

```just
# CI-specific commands
ci-setup:
    @_info "Setting up CI environment..."
    just setup --ci

ci-test:
    @_info "Running CI tests..."
    just check
    just test-all

ci-build:
    @_info "Building for CI..."
    just build --production
```

### 3. Project Templates

```just
# Create new package from template
new-package NAME TYPE="node":
    #!/usr/bin/env bash
    case {{TYPE}} in
        node)
            cp -r templates/node-service packages/{{NAME}}
            ;;
        python)
            cp -r templates/python-service packages/{{NAME}}
            ;;
        *)
            echo "Unknown type: {{TYPE}}"
            exit 1
            ;;
    esac
    echo "✅ Created new {{TYPE}} package: {{NAME}}"
```

## Best Practices

1. **Consistent Naming**: Use `::` for module commands, `-` for multi-word commands
2. **Help Commands**: Every module should have a `help` recipe
3. **Descriptions**: Use comments above recipes for `--list` descriptions
4. **Error Handling**: Use `_has` to check for required tools
5. **Confirmations**: Use `_confirm` for destructive operations
6. **Progress Indicators**: Use `_info`, `_warn`, `_error` for feedback
7. **Aliases**: Provide short aliases for common commands
8. **Environment**: Use `.env` files for configuration

## Usage Examples

```bash
# Get started
just help                  # Show beautiful help menu
just setup                 # Setup everything

# Daily development
just dev                   # Start all services
just in api test          # Run tests in API package
just api::dev             # Start only API in dev mode

# Testing
just test-all             # Run all tests
just test::integration    # Run integration tests
just api::test-file user  # Test specific file

# Docker operations
just docker::up           # Start containers
just docker::logs api     # Show API logs
just docker::exec db psql # Access database

# Deployment
just deploy::staging      # Deploy to staging
just deploy::production   # Deploy to production
```

This system provides maximum developer friendliness while remaining scalable for large monorepos.