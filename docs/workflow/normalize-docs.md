# Documentation Normalization Workflow

## Overview

This workflow ensures all documentation remains consistent with the current project structure, code functionality, and inter-document relationships. It should be run regularly and especially after major changes.

## When to Run This Workflow

### Mandatory (Must Run)
- After major refactoring or restructuring
- Before releases or major deployments
- When onboarding new team members
- After API changes or additions

### Recommended (Should Run)
- Weekly during active development
- After adding new features
- When documentation inconsistencies are reported
- Before writing new documentation that references existing docs

## Workflow Steps

### Step 1: Prepare Environment
```bash
# Ensure project is up to date
git pull origin main

# Start services for testing
just bootstrap
just run-docker-d

# Install documentation tools
pip install -r requirements-docs.txt
```

### Step 2: Run Automated Scans
```bash
# Scan all documentation files
python scripts/scan-docs.py --output scan-results.json

# Generate consistency report
python scripts/generate-consistency-report.py scan-results.json \
  --output consistency-report.md

# Run documentation tests
pytest tests/test_documentation.py -v
```

### Step 3: Manual Review Process

#### 3.1 Review Scan Results
Open `consistency-report.md` and examine:
- **Critical Issues**: Broken commands, missing files, invalid links
- **Warning Issues**: Outdated examples, version mismatches
- **Info Issues**: Style inconsistencies, minor improvements

#### 3.2 Test Key Workflows
Manually test documented workflows:
```bash
# Test setup procedures
just clean && just bootstrap

# Test core workflows
just run
just test
just check

# Test docker workflows
just run-docker-d
just test-docker
```

#### 3.3 Verify External Dependencies
Check that external references are still valid:
- Package versions in requirements
- API endpoint references
- Tool installation instructions
- System requirements

### Step 4: Create Re-integration Plan

For each inconsistency found:

#### 4.1 Categorize Issues
```markdown
## Critical Issues (Fix Immediately)
- [ ] Broken command in setup guide
- [ ] Missing file referenced in architecture docs

## Important Issues (Fix This Sprint)
- [ ] Outdated API examples in REST docs
- [ ] Wrong directory structure in README

## Minor Issues (Fix When Convenient)
- [ ] Inconsistent formatting in code blocks
- [ ] Outdated package versions mentioned
```

#### 4.2 Group Related Fixes
```markdown
## Fix Groups

### Group 1: Project Structure Updates
- Update all path references from old structure
- Fix import statements in examples
- Correct directory navigation instructions

### Group 2: API Documentation Updates
- Update endpoint examples
- Fix request/response samples
- Correct GraphQL schema references

### Group 3: Command Updates
- Fix Just command examples
- Update Docker commands
- Correct CLI usage examples
```

#### 4.3 Estimate Effort
```markdown
## Effort Estimates

### Quick Fixes (< 1 hour)
- Path corrections
- Command updates
- Link fixes

### Medium Fixes (1-4 hours)
- API example updates
- Code example rewrites
- Section reorganization

### Large Fixes (> 4 hours)
- Complete workflow rewrites
- New documentation sections
- Complex restructuring
```

### Step 5: User Review and Approval

#### 5.1 Present Findings
Create a summary document with:
- Total issues found
- Breakdown by category
- Proposed re-integration plan
- Estimated timeline

#### 5.2 Get User Input
Present to user for approval:
```markdown
## Documentation Audit Results

### Summary
- **Total Issues**: 23
- **Critical**: 3
- **Important**: 12
- **Minor**: 8

### Proposed Plan
1. **Phase 1** (Critical): Fix broken commands and missing files
2. **Phase 2** (Important): Update API docs and examples
3. **Phase 3** (Minor): Style and formatting improvements

### Timeline
- Phase 1: 2 hours
- Phase 2: 6 hours
- Phase 3: 3 hours

**Total Estimated Time**: 11 hours

### Questions for User
1. Are there any issues that should be deprioritized?
2. Are there additional consistency requirements?
3. Should any fixes be handled differently?
```

### Step 6: Execute Approved Changes

#### 6.1 Work in Priority Order
Start with critical issues first:
```bash
# Fix critical issues
git checkout -b fix/critical-docs-issues
# Make fixes...
git commit -m "fix: resolve critical documentation issues"

# Fix important issues
git checkout -b fix/important-docs-updates
# Make fixes...
git commit -m "docs: update API examples and project structure"

# Fix minor issues
git checkout -b fix/minor-docs-cleanup
# Make fixes...
git commit -m "docs: cleanup formatting and minor inconsistencies"
```

#### 6.2 Test Each Fix
After each group of fixes:
```bash
# Re-run scans
python scripts/scan-docs.py --output scan-results-updated.json

# Test affected workflows
just clean && just bootstrap
# Test specific workflows that were updated
```

#### 6.3 Update Tracking Documents
After fixes are complete:
```bash
# Update work log
# Add entry to docs/project-management/work-log.md

# Update todo list
# Mark documentation audit as complete

# Update roadmap if needed
# Note any follow-up work required
```

### Step 7: Validation and Monitoring

#### 7.1 Final Validation
```bash
# Run full test suite
pytest tests/test_documentation.py

# Generate final report
python scripts/generate-consistency-report.py scan-results-final.json \
  --output final-consistency-report.md

# Manual spot checks
# Review 5-10 random documentation files
```

#### 7.2 Set Up Monitoring
```bash
# Add to CI/CD pipeline
# .github/workflows/docs-check.yml

# Set up periodic checks
# Add to weekly/monthly maintenance tasks
```

## Tools and Scripts

### Required Tools
- `scripts/scan-docs.py` - Automated scanner
- `scripts/generate-consistency-report.py` - Report generator
- `tests/test_documentation.py` - Automated tests
- `requirements-docs.txt` - Documentation tools

### Optional Enhancements
- `scripts/fix-common-issues.py` - Auto-fix common problems
- `scripts/validate-examples.py` - Test code examples
- `scripts/check-external-links.py` - Validate external references

## Best Practices

### For Maintainers
1. **Always test examples before documenting them**
2. **Use relative paths in documentation**
3. **Keep command examples up to date**
4. **Cross-reference related sections**
5. **Update docs immediately after code changes**

### For Contributors
1. **Run documentation tests before submitting PRs**
2. **Update relevant docs when changing code**
3. **Follow existing documentation patterns**
4. **Test all documented procedures**

## Success Metrics

### Immediate Success
- All documented commands work
- All file paths are valid
- All code examples compile/run
- All internal links resolve

### Long-term Success
- New team members can follow setup guides
- Documentation stays current with code
- Fewer support questions about setup
- Increased developer productivity

## Troubleshooting

### Common Issues
1. **Scan script fails**: Check Python dependencies
2. **Commands don't work**: Verify environment setup
3. **Links broken**: Check file movements/renames
4. **Examples fail**: Verify import paths and API changes

### Getting Help
- Review existing documentation tests
- Check work log for similar issues
- Consult with team members
- Update this workflow if needed

---

*This workflow should be updated when new documentation patterns emerge or when the project structure changes significantly.*