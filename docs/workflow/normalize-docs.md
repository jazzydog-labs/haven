# Documentation Normalization Workflow

## Overview

This workflow ensures all documentation remains accurate and consistent with the current project state. It should be run periodically or after major changes.

## When to Use

- After significant code refactoring
- When adding new features or modules
- Before major releases
- When documentation feels out of sync
- Monthly as routine maintenance

## Prerequisites

- Python 3.8+ installed
- Access to project root directory
- Just command available
- Understanding of project structure

## Steps

### 1. Run Documentation Scanner

```bash
# Generate audit report
python scripts/scan-docs.py --output docs/documentation-audit-report.md

# View summary in terminal
python scripts/scan-docs.py --format markdown | head -50
```

### 2. Review Audit Report

Open `docs/documentation-audit-report.md` and review:
- Summary statistics
- Issues by type
- Files with most issues
- Severity of problems

### 3. Categorize Issues

Group issues into categories:

#### Quick Fixes (< 5 minutes each)
- Updated command syntax (e.g., `just db-up` → `just database::up`)
- Localhost URLs → domain names
- Simple path corrections

#### Medium Fixes (5-30 minutes each)
- Broken internal links
- Outdated code examples
- Missing documentation references

#### Major Updates (> 30 minutes)
- Architectural changes
- Complete section rewrites
- New feature documentation

### 4. Create Fix Plan

```markdown
# Documentation Fix Plan - [DATE]

## Priority 1: Breaking Issues
- [ ] Fix invalid commands preventing user progress
- [ ] Update critical path documentation

## Priority 2: User Experience
- [ ] Update all localhost URLs to domains
- [ ] Fix broken internal links
- [ ] Correct code examples

## Priority 3: Consistency
- [ ] Align terminology across docs
- [ ] Update file paths
- [ ] Standardize formatting
```

### 5. Execute Fixes

#### Automated Fixes

For common patterns, use sed or similar tools:

```bash
# Update old Just commands to new module syntax
find docs -name "*.md" -exec sed -i.bak 's/just db-up/just database::up/g' {} \;
find docs -name "*.md" -exec sed -i.bak 's/just run-docker/just docker::up/g' {} \;

# Update localhost URLs
find docs -name "*.md" -exec sed -i.bak 's|http://localhost:3000|http://web.haven.local|g' {} \;
find docs -name "*.md" -exec sed -i.bak 's|http://localhost:8080|http://api.haven.local|g' {} \;
```

#### Manual Fixes

1. Open each file with issues
2. Search for flagged line numbers
3. Apply appropriate fix
4. Verify fix is correct

### 6. Validate Fixes

```bash
# Re-run scanner
python scripts/scan-docs.py --output docs/documentation-audit-report-fixed.md

# Compare before/after
diff docs/documentation-audit-report.md docs/documentation-audit-report-fixed.md
```

### 7. Test Documentation

For critical documentation:

1. **Setup guides**: Follow steps on clean system
2. **API examples**: Run actual commands
3. **Code snippets**: Verify they compile/run
4. **Links**: Click through navigation paths

### 8. Update Tracking

```bash
# Add work log entry
echo "## $(date +%Y-%m-%d).NNNN - Documentation normalization
**Updated**: Fixed N documentation inconsistencies
**See**: docs/documentation-audit-report.md for details
**Test**: python scripts/scan-docs.py
**Demo**: All commands now use new module syntax" >> docs/project-management/work-log.md
```

## Common Fixes Reference

### Command Updates

Old → New mappings:
```
just db-up           → just database::up
just db-migrate      → just database::migrate
just db-console      → just database::console
just run-docker      → just docker::up
just stop-docker     → just docker::down
just test-python     → just testing::python
just test-web        → just testing::web
```

### URL Updates

Development URLs:
```
http://localhost:3000      → http://web.haven.local
http://localhost:8080      → http://api.haven.local
http://localhost:8080/docs → http://api.haven.local/docs
```

### Path Updates

Project structure:
```
src/haven/         → apps/api/src/haven/
tests/             → apps/api/tests/
frontend/          → apps/web/
```

## Automation Ideas

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: check-docs
        name: Check documentation consistency
        entry: python scripts/scan-docs.py
        language: system
        files: '\.md$'
```

### CI Integration

```yaml
# .github/workflows/docs.yml
name: Documentation Check
on: [pull_request]
jobs:
  check-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run documentation scanner
        run: |
          python scripts/scan-docs.py --output report.md
          if grep -q "Total Issues: 0" report.md; then
            echo "✅ Documentation is consistent"
          else
            echo "❌ Documentation issues found"
            cat report.md
            exit 1
          fi
```

## Maintenance Schedule

- **Weekly**: Quick scan for broken commands
- **Bi-weekly**: Fix localhost URLs and paths
- **Monthly**: Full audit and normalization
- **Quarterly**: Architecture documentation review

## Tools and Scripts

- `scripts/scan-docs.py` - Main scanning tool
- `scripts/fix-common-docs.sh` - Automated fixes (to be created)
- `tests/test_documentation.py` - Documentation tests (to be created)

## Definition of Done

- [ ] Scanner reports 0 critical issues
- [ ] All commands are valid and tested
- [ ] All internal links work
- [ ] Code examples compile/run
- [ ] URLs use proper domain names
- [ ] Work log updated
- [ ] Commit with clear message