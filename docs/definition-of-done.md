# Haven - Definition of Done

*Last updated: 2025-07-16*

A feature or task is considered **DONE** when ALL of the following criteria are met:

---

## 1. Code Quality Gates ✅

### Linting
- **Tool**: Ruff
- **Command**: `just lint`
- **Requirement**: 0 errors, 0 warnings
- **Config**: `pyproject.toml` [tool.ruff] section

### Type Checking
- **Tool**: Pyright (strict mode)
- **Command**: `just type`
- **Requirement**: All type checks pass
- **Config**: `pyproject.toml` [tool.pyright] section

### Testing
- **Tool**: pytest with coverage
- **Command**: `just test`
- **Requirements**:
  - All tests pass
  - Code coverage ≥ 70%
  - New features have corresponding tests
  - Edge cases are covered

### Documentation Build
- **Tool**: MkDocs
- **Command**: `just docs`
- **Requirement**: Documentation builds without errors
- **Includes**: Updated API docs if endpoints changed

---

## 2. Feature Demonstration 🎯

### Demo Creation
- **Command**: `just demo` (if applicable)
- **Requirements**:
  - Shows the feature in action
  - Highlights high-impact capabilities
  - Gets "wow!" response from stakeholders
  - Includes usage instructions

### Demo Checklist
- [ ] Core functionality demonstrated
- [ ] Error handling shown
- [ ] Performance is acceptable
- [ ] User experience is smooth

---

## 3. Documentation Updates 📚

### Code Documentation
- [ ] Docstrings for public APIs
- [ ] Type hints on all functions
- [ ] Complex logic has inline comments

### Project Documentation
- [ ] Feature documented in relevant `.md` files
- [ ] API changes reflected in `docs/api/`
- [ ] Architecture decisions recorded if applicable
- [ ] CLAUDE.md updated if development workflow changed

---

## 4. Version Control 🔄

### Commit Requirements
- [ ] **Commit immediately after task completion** - Don't batch multiple tasks
- [ ] Atomic commits with clear messages
- [ ] Follows conventional commit format
- [ ] No merge conflicts
- [ ] Branch is up-to-date with main

**Important**: Always commit completed work before moving to the next task. This ensures:
- Clear history of what was done when
- Ability to rollback specific changes
- Easier debugging if issues arise
- Better collaboration with team members

### Pre-commit Checks
- [ ] All pre-commit hooks pass
- [ ] No secrets or credentials committed
- [ ] File permissions are correct

---

## 5. Integration Verification 🔗

### Local Testing
- [ ] Feature works with `just run`
- [ ] Database migrations applied cleanly
- [ ] No regression in existing features

### API Testing
- [ ] REST endpoints tested via Swagger UI
- [ ] GraphQL queries work in GraphiQL
- [ ] Response formats match specification

---

## 6. Quick Checklist Commands

Run all quality gates in sequence:
```bash
just check  # Runs lint, type, test
```

Individual checks:
```bash
just lint   # Ruff linting
just type   # Pyright type checking
just test   # pytest with coverage
just docs   # Build documentation
```

---

## 7. Exceptions

Tasks may skip certain criteria with explicit justification:

- **Prototypes**: May skip documentation requirements
- **Bug fixes**: May skip demo requirement
- **Documentation**: May skip code coverage requirement
- **Infrastructure**: May have different testing requirements

Always document exceptions in the PR description.

---

Remember: **Done means ready for production**, not just "works on my machine"!

## 8. Workflow Summary

1. Pick a task from `todo.md` or `docs/roadmap.md`
2. Implement the feature/fix
3. Run quality gates (`just check`)
4. Update relevant documentation
5. **Commit your changes immediately**
6. Move to the next task

Never leave completed work uncommitted - each task should result in at least one commit!