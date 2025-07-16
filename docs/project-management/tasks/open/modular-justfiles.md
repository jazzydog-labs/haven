# Task: Modularize Justfile into Package-Specific Files

## Description
Break down the monolithic justfile into smaller, modular justfiles organized by package and functionality. This will improve maintainability and allow each package to manage its own build/test/deployment commands independently.

## Acceptance Criteria
- [ ] Create package-specific justfiles for each Python/TypeScript package
- [ ] Create dedicated justfile for demo commands
- [ ] Maintain backward compatibility with existing `just` commands
- [ ] Ensure proper import/inclusion between justfiles
- [ ] Update documentation to reflect new justfile structure
- [ ] Test that all existing commands still work after refactoring

## Implementation Notes

### Proposed Structure
```
justfile                    # Main orchestrator, imports others
api/justfile               # Python API package commands
client/justfile            # React/TypeScript client commands
justfile.demos             # Demo commands (just demo-*)
justfile.common            # Shared utilities and variables
```

### Command Organization
- **Main justfile**: High-level orchestration, bootstrap, environment setup
- **api/justfile**: Python-specific commands (test, lint, type-check, migrations)
- **client/justfile**: TypeScript/React commands (build, test, lint, dev server)
- **justfile.demos**: All `just demo-*` commands for feature demonstrations
- **justfile.common**: Shared variables, Docker commands, database operations

### Import Strategy
- Use `import` statements to include package-specific justfiles
- Maintain consistent command naming across packages
- Allow package-specific overrides where needed

## Technical Considerations
- Justfile import syntax and path resolution
- Variable scoping between imported justfiles
- Command namespacing (e.g., `just api:test` vs `just test`)
- Cross-package dependencies and orchestration
- CI/CD pipeline compatibility

## Definition of Done
- [ ] Justfiles are split into logical, package-based modules
- [ ] All existing commands work unchanged for backward compatibility
- [ ] New package-specific commands are properly namespaced
- [ ] Demo commands are centralized in justfile.demos
- [ ] Documentation updated in CLAUDE.md and relevant docs
- [ ] CI/CD scripts updated if needed
- [ ] All team members can run commands without issues
- [ ] Performance of justfile execution is maintained or improved