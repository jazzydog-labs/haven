# Common variables and utilities for all justfiles

# Colors for output
export RED := '\033[0;31m'
export GREEN := '\033[0;32m'
export YELLOW := '\033[0;33m'
export BLUE := '\033[0;34m'
export CYAN := '\033[0;36m'
export NC := '\033[0m' # No Color
export BOLD := '\033[1m'

# Project paths
export PROJECT_ROOT := justfile_directory()
export API_DIR := PROJECT_ROOT / "apps/api"
export WEB_DIR := PROJECT_ROOT / "apps/web"

# Python environment
export PYTHON := API_DIR / ".venv/bin/python"
export PIP := API_DIR / ".venv/bin/pip"

# Utility functions
_info MSG:
    @echo "${BLUE}ℹ${NC}  {{ MSG }}"

_warn MSG:
    @echo "${YELLOW}⚠${NC}  {{ MSG }}"

_error MSG:
    @echo "${RED}✗${NC}  {{ MSG }}"

_success MSG:
    @echo "${GREEN}✓${NC}  {{ MSG }}"

_confirm MSG:
    @echo "${YELLOW}?${NC}  {{ MSG }} [y/N] " && read ans && [ $${ans:-N} = y ]

# Check if a command exists
_has CMD:
    @command -v {{ CMD }} >/dev/null 2>&1 || { _error "{{ CMD }} is not installed"; exit 1; }

# Section header for output
_section TITLE:
    @echo ""
    @echo "${BOLD}=== {{ TITLE }} ===${NC}"
    @echo ""