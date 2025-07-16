#!/usr/bin/env bash
# Beautiful help system for Haven justfiles

set -e

# Colors
BOLD='\033[1m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
DIM='\033[2m'
NC='\033[0m'

echo -e "${BOLD}🏗️  Haven Development Commands${NC}"
echo -e "${DIM}================================${NC}"
echo ""

# Function to format command help
format_section() {
    local section="$1"
    local prefix="$2"
    echo -e "${BOLD}${BLUE}$section${NC}"
    echo ""
}

# Function to format command
format_cmd() {
    local cmd="$1"
    local desc="$2"
    printf "  ${GREEN}%-25s${NC} %s\n" "$cmd" "$desc"
}

# Core Commands
format_section "🚀 Quick Start"
format_cmd "just" "Show this help (interactive mode)"
format_cmd "just run" "Start everything (frontend + backend)"
format_cmd "just run-proxy" "Start with local domains (haven.local)"
format_cmd "just stop-all" "Stop all services"
echo ""

# Development
format_section "💻 Development"
format_cmd "just bootstrap" "Set up development environment"
format_cmd "just check" "Run all quality checks"
format_cmd "just test" "Run all tests"
format_cmd "just lint" "Run linting"
format_cmd "just format" "Format code"
echo ""

# Docker
format_section "🐳 Docker"
format_cmd "just docker::up" "Start containers"
format_cmd "just docker::down" "Stop containers"
format_cmd "just docker::logs" "View logs"
format_cmd "just docker::rebuild" "Rebuild images"
echo ""

# Database
format_section "🗄️  Database"
format_cmd "just database::up" "Start PostgreSQL"
format_cmd "just database::migrate" "Run migrations"
format_cmd "just database::console" "Database console"
format_cmd "just database::reset" "Reset database"
echo ""

# Testing
format_section "🧪 Testing"
format_cmd "just testing::all" "Run all tests"
format_cmd "just testing::python" "Run Python tests"
format_cmd "just testing::web" "Run web tests"
format_cmd "just testing::watch" "Run tests in watch mode"
echo ""

# Package-specific
format_section "📦 Packages"
format_cmd "just api::<cmd>" "API-specific commands"
format_cmd "just web::<cmd>" "Web-specific commands"
echo ""

# Tips
echo -e "${BOLD}${YELLOW}💡 Tips:${NC}"
echo -e "  • Use ${CYAN}just --list${NC} for all commands"
echo -e "  • Use ${CYAN}just --choose${NC} for interactive mode"
echo -e "  • Use ${CYAN}just <module>::help${NC} for module help"
echo -e "  • Tab completion available (see docs)"
echo ""