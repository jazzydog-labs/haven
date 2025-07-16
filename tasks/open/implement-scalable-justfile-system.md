# Implement Scalable Justfile System

## Description
Transform the current Justfile architecture to follow the scalable monorepo pattern described in `docs/development/scalable-justfile.md`. This will create a hierarchical, discoverable, and maintainable command structure with proper modularization.

## Acceptance Criteria
- [ ] Hierarchical justfile structure implemented
- [ ] All existing commands preserved and working
- [ ] New command discovery system in place
- [ ] Beautiful help system with categorized commands
- [ ] Shell completions working
- [ ] All justfiles tested and validated
- [ ] Test results tracked in `tests/justfile-validation.json`
- [ ] Documentation updated

## Current State Analysis

### Existing Structure
```
/
├── Justfile                    # Main orchestrator (partially modular)
├── justfile.common            # Shared variables
├── justfile.database          # Database operations
├── justfile.docker            # Docker commands
├── justfile.demos             # Demo commands
├── apps/api/justfile          # API-specific commands
└── apps/web/justfile          # Web-specific commands
```

### Target Structure
```
/
├── justfile                   # Main entry point with discovery
├── .just/                     # Just utilities directory
│   ├── common.just           # Shared recipes/variables
│   ├── help.sh              # Help formatting script
│   ├── completions.sh       # Shell completions
│   └── test-commands.sh     # Command validation script
├── tools/                     # Tool-specific justfiles
│   ├── docker.just          # Docker operations
│   ├── database.just        # Database operations
│   ├── testing.just         # Testing commands
│   └── demos.just           # Demo commands
└── apps/                     # Package-specific justfiles
    ├── api/justfile         # API commands
    └── web/justfile         # Web commands
```

## Implementation Steps

### Phase 1: Core Infrastructure
1. **Create .just/ directory structure**
   ```bash
   mkdir -p .just
   touch .just/common.just
   touch .just/help.sh
   touch .just/completions.sh
   touch .just/test-commands.sh
   ```

2. **Migrate shared utilities to .just/common.just**
   - Move variables from justfile.common
   - Add helper functions (_info, _warn, _error, _confirm)
   - Add command checking (_has)
   - Add color definitions

3. **Create tools/ directory**
   ```bash
   mkdir -p tools
   ```

### Phase 2: Command Migration
1. **Migrate to tools/ structure**
   - `justfile.docker` → `tools/docker.just`
   - `justfile.database` → `tools/database.just`
   - `justfile.demos` → `tools/demos.just`
   - Create `tools/testing.just` for test commands

2. **Update main justfile**
   - Use `mod` syntax for importing tools
   - Add interactive `--choose` as default
   - Add beautiful help system
   - Add command discovery

3. **Update package justfiles**
   - `apps/api/justfile` - standardize with help system
   - `apps/web/justfile` - standardize with help system

### Phase 3: Enhanced Features
1. **Beautiful help system**
   - Implement `.just/help.sh` with formatted output
   - Add categorized command listings
   - Include usage examples and tips

2. **Shell completions**
   - Implement bash/zsh completions
   - Support module:: completion
   - Add to setup documentation

3. **Command validation system**
   - Create comprehensive test script
   - Test every command in every justfile
   - Generate test results JSON

## Command Mapping

### Current → Target Command Structure

**Root Commands:**
- `just help` → Enhanced help with categories
- `just setup` → `just setup` (orchestrates all)
- `just dev` → `just dev` (starts all services)
- `just test-all` → `just test::all`
- `just clean` → `just clean` (orchestrates all)

**Docker Commands:**
- `just run-docker` → `just docker::up`
- `just stop-docker` → `just docker::down`
- `just logs-docker` → `just docker::logs`
- `just rebuild-docker` → `just docker::rebuild`

**Database Commands:**
- `just db-up` → `just database::up`
- `just db-migrate` → `just database::migrate`
- `just db-console` → `just database::console`
- `just db-reset` → `just database::reset`

**Testing Commands:**
- `just test` → `just test::all`
- `just test-python` → `just test::python`
- `just test-web` → `just test::web`
- `just test-docker` → `just test::docker`

**Package Commands:**
- `just run-api` → `just api::dev`
- `just run-web` → `just web::dev`
- `just lint-python` → `just api::lint`
- `just lint-web` → `just web::lint`

## Testing Strategy

### Automated Command Testing
Create `.just/test-commands.sh`:
```bash
#!/usr/bin/env bash
# Test all just commands and generate results

RESULTS_FILE="tests/justfile-validation.json"
mkdir -p tests

echo "Testing all just commands..."
echo '{"timestamp": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'", "results": [' > "$RESULTS_FILE"

# Test function
test_command() {
    local cmd="$1"
    local expected_result="$2"
    
    echo "  Testing: $cmd"
    
    if timeout 10s just --dry-run $cmd &>/dev/null; then
        status="pass"
    else
        status="fail"
    fi
    
    echo "    {\"command\": \"$cmd\", \"status\": \"$status\", \"expected\": \"$expected_result\"}," >> "$RESULTS_FILE"
}

# Test all commands systematically
test_root_commands() {
    test_command "help" "pass"
    test_command "setup" "pass"
    test_command "dev" "pass"
    test_command "clean" "pass"
    test_command "test-all" "pass"
}

test_docker_commands() {
    test_command "docker::help" "pass"
    test_command "docker::up" "pass"
    test_command "docker::down" "pass"
    test_command "docker::logs" "pass"
}

test_database_commands() {
    test_command "database::help" "pass"
    test_command "database::up" "pass"
    test_command "database::migrate" "pass"
    test_command "database::console" "pass"
}

test_package_commands() {
    test_command "api::help" "pass"
    test_command "api::test" "pass"
    test_command "api::dev" "pass"
    test_command "web::help" "pass"
    test_command "web::test" "pass"
    test_command "web::dev" "pass"
}

# Run all tests
test_root_commands
test_docker_commands
test_database_commands
test_package_commands

# Close JSON
echo '    {"command": "validation-complete", "status": "complete", "expected": "pass"}' >> "$RESULTS_FILE"
echo ']}' >> "$RESULTS_FILE"

echo "✅ Command validation complete. Results in $RESULTS_FILE"
```

### Manual Validation Checklist
- [ ] All commands show in `just --list`
- [ ] Help commands work for all modules
- [ ] Interactive `just --choose` works
- [ ] Shell completions work
- [ ] All existing workflows preserved
- [ ] New command structure is intuitive

## File Structure Changes

### Files to Create
- `.just/common.just` - Shared utilities
- `.just/help.sh` - Beautiful help system
- `.just/completions.sh` - Shell completions
- `.just/test-commands.sh` - Command validation
- `tools/docker.just` - Docker commands
- `tools/database.just` - Database commands
- `tools/testing.just` - Testing commands
- `tools/demos.just` - Demo commands
- `tests/justfile-validation.json` - Test results

### Files to Update
- `justfile` - Main orchestrator
- `apps/api/justfile` - API commands
- `apps/web/justfile` - Web commands
- `CLAUDE.md` - Update command examples
- `docs/development/justfile-architecture.md` - Update docs

### Files to Remove
- `justfile.common`
- `justfile.database`
- `justfile.docker`
- `justfile.demos`

## Backwards Compatibility

### Transition Strategy
1. **Phase 1**: Implement new structure alongside old
2. **Phase 2**: Add deprecated command warnings
3. **Phase 3**: Remove old commands after validation

### Deprecated Command Handling
```just
# Add to main justfile during transition
run-docker:
    @echo "⚠️  DEPRECATED: Use 'just docker::up' instead"
    @just docker::up

stop-docker:
    @echo "⚠️  DEPRECATED: Use 'just docker::down' instead"
    @just docker::down
```

## Documentation Updates

### Files to Update
- `CLAUDE.md` - Update all command examples
- `docs/development/justfile-architecture.md` - Document new structure
- `docs/development/scalable-justfile.md` - Mark as implemented
- `README.md` - Update quick start commands

### New Documentation
- `.just/README.md` - Explain utility functions
- `tools/README.md` - Document tool modules
- Shell completion setup guide

## Definition of Done
- [ ] All new justfile structure implemented
- [ ] All existing commands preserved and working
- [ ] Beautiful help system implemented
- [ ] Shell completions working
- [ ] Command validation script created
- [ ] Test results JSON generated and validates all commands
- [ ] Documentation updated with new command structure
- [ ] Team can use new command discovery features
- [ ] Backwards compatibility maintained during transition
- [ ] Old files removed after validation
- [ ] Work log entry added with demo commands
- [ ] CLAUDE.md updated with new command structure