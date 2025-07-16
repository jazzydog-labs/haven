# Documentation Fix Plan - 2025-07-16

## Overview

The documentation audit found 946 issues across 65 files. This plan prioritizes fixes to restore documentation accuracy and improve developer experience.

## Summary of Issues

- **Invalid Paths**: 646 (mostly false positives from URL fragments and placeholders)
- **Invalid Commands**: 188 (critical - prevents users from following docs)
- **Broken Links**: 33 (impacts navigation)
- **Localhost URLs**: 79 (should use domain names)

## Priority 1: Breaking Issues (Fix Immediately)

### Invalid Just Commands
All Just commands need updating to new module syntax:

**Files to fix:**
- CLAUDE.md
- README.md  
- docs/quickstart.md
- docs/development/*.md
- docs/api/*.md
- apps/*/README.md

**Common replacements:**
```
just database::up           → just database::up
just database::migrate      → just database::migrate
just database::console      → just database::console
just database::make         → just database::make
just database::reset        → just database::reset

just docker::up      → just docker::up
just docker::up-d    → just docker::up-d
just docker::down     → just docker::down
just docker::logs     → just docker::logs
just docker::ps       → just docker::ps
just docker::shell    → just docker::shell
just docker::rebuild  → just docker::rebuild
just docker::reset    → just docker::reset

just testing::python     → just testing::python
just testing::web        → just testing::web
just testing::fast       → just testing::fast
just docker::test     → just docker::test

just docker::lint     → just docker::lint
just docker::type-check    → just docker::type-check
```

## Priority 2: User Experience

### Update Localhost URLs
Replace all localhost references with domain names:

```
http://web.haven.local      → http://web.haven.local
http://api.haven.local      → http://api.haven.local
http://api.haven.local/docs  → http://api.haven.local/docs
http://api.haven.local/graphql → http://api.haven.local/graphql
http://docs.haven.local      → http://docs.haven.local
```

### Fix Broken Internal Links
- Update paths to match new docs structure
- Fix references to moved files
- Correct anchor links

## Priority 3: Consistency Updates

### Path Updates
Many path issues are false positives, but these need fixing:
- `src/haven/` → `apps/api/src/haven/`
- `tests/` → `apps/api/tests/`
- References to old project structure

### Remove Invalid Path False Positives
The scanner flagged many non-path strings as paths:
- URL fragments like `//github.com/`
- Placeholders like `YYYY-MM-DD.NNNN`
- Type definitions like `async/await`
- Headers like `Tools/Commands`

These can be ignored.

## Execution Plan

### Phase 1: Automated Command Updates (30 minutes)

```bash
# Create backup
cp -r docs docs.backup
cp CLAUDE.md CLAUDE.md.backup
cp README.md README.md.backup

# Update Just commands
find . -name "*.md" -exec sed -i.bak 's/just database::up/just database::up/g' {} \;
find . -name "*.md" -exec sed -i.bak 's/just database::migrate/just database::migrate/g' {} \;
find . -name "*.md" -exec sed -i.bak 's/just database::console/just database::console/g' {} \;
find . -name "*.md" -exec sed -i.bak 's/just database::make/just database::make/g' {} \;
find . -name "*.md" -exec sed -i.bak 's/just database::reset/just database::reset/g' {} \;

find . -name "*.md" -exec sed -i.bak 's/just docker::up-d/just docker::up-d/g' {} \;
find . -name "*.md" -exec sed -i.bak 's/just docker::up/just docker::up/g' {} \;
find . -name "*.md" -exec sed -i.bak 's/just docker::down/just docker::down/g' {} \;
find . -name "*.md" -exec sed -i.bak 's/just docker::logs/just docker::logs/g' {} \;
find . -name "*.md" -exec sed -i.bak 's/just docker::ps/just docker::ps/g' {} \;
find . -name "*.md" -exec sed -i.bak 's/just docker::shell/just docker::shell/g' {} \;
find . -name "*.md" -exec sed -i.bak 's/just docker::rebuild/just docker::rebuild/g' {} \;
find . -name "*.md" -exec sed -i.bak 's/just docker::reset/just docker::reset/g' {} \;

find . -name "*.md" -exec sed -i.bak 's/just testing::python/just testing::python/g' {} \;
find . -name "*.md" -exec sed -i.bak 's/just testing::web/just testing::web/g' {} \;
find . -name "*.md" -exec sed -i.bak 's/just testing::fast/just testing::fast/g' {} \;
find . -name "*.md" -exec sed -i.bak 's/just docker::test/just docker::test/g' {} \;

find . -name "*.md" -exec sed -i.bak 's/just docker::lint/just docker::lint/g' {} \;
find . -name "*.md" -exec sed -i.bak 's/just docker::type-check/just docker::type-check/g' {} \;

# Fix special cases
find . -name "*.md" -exec sed -i.bak 's/just api::add-entity/just api::add-entity/g' {} \;

# Clean up backup files
find . -name "*.bak" -delete
```

### Phase 2: URL Updates (15 minutes)

```bash
# Update localhost URLs
find . -name "*.md" -exec sed -i.bak 's|http://web.haven.local|http://web.haven.local|g' {} \;
find . -name "*.md" -exec sed -i.bak 's|http://api.haven.local|http://api.haven.local|g' {} \;
find . -name "*.md" -exec sed -i.bak 's|docs.haven.local|docs.haven.local|g' {} \;

# Clean up
find . -name "*.bak" -delete
```

### Phase 3: Manual Review (1 hour)

1. Review CLAUDE.md for accuracy
2. Update README.md quickstart
3. Fix broken internal links in docs/
4. Update any remaining path references

### Phase 4: Validation (15 minutes)

```bash
# Re-run scanner
python scripts/scan-docs.py --output docs/documentation-audit-report-fixed.md

# Test critical commands
just help
just database::up
just docker::up
just testing::all

# Verify URLs work
curl http://api.haven.local/health
```

## Success Criteria

- [ ] All Just commands use new module syntax
- [ ] No localhost URLs remain (except in examples)
- [ ] Critical user paths (setup, run, test) work
- [ ] Scanner shows < 100 issues (mostly false positives)
- [ ] README quickstart is accurate
- [ ] CLAUDE.md daily workflow works

## Timeline

- Phase 1: 30 minutes (automated)
- Phase 2: 15 minutes (automated)
- Phase 3: 60 minutes (manual)
- Phase 4: 15 minutes (validation)

**Total: ~2 hours**

## Next Steps

1. Get approval for this plan
2. Execute phases 1-2 (automated fixes)
3. Review changes
4. Complete manual fixes
5. Validate and test
6. Commit with detailed message
7. Update work log