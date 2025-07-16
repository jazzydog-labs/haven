# Comprehensive Documentation Audit and Normalization

## Description
Perform a complete audit of all documentation files (README.md, docs/*, CLAUDE.md, etc.) to ensure they accurately reflect the current project structure, code functionality, and inter-document relationships. Create a systematic process for maintaining documentation consistency.

## Acceptance Criteria
- [ ] All documentation files audited and cataloged
- [ ] Inconsistencies identified and documented
- [ ] Re-integration plan created for each inconsistency
- [ ] Automated checks implemented where possible
- [ ] Workflow documented in `docs/workflow/normalize-docs.md`
- [ ] User approval obtained for re-integration plan

## Scope of Audit

### Documentation Files to Review
```
README.md
CLAUDE.md
SECURITY.md
LICENSE

docs/
├── overview.md
├── quickstart.md
├── index.md
├── architecture/
│   └── architecture.md
├── api/
│   ├── rest.md
│   ├── graphql.md
│   ├── openapi.md
│   └── diff-generation.md
├── development/
│   ├── local-setup.md
│   ├── testing.md
│   ├── quality.md
│   ├── configuration.md
│   ├── alembic.md
│   ├── refactoring.md
│   ├── definition-of-done.md
│   ├── tasks-workflow.md
│   └── justfile-architecture.md
├── operations/
│   ├── docker.md
│   ├── deployment.md
│   ├── monitoring.md
│   └── cli.md
├── project-management/
│   ├── spec.md
│   ├── roadmap.md
│   ├── commits-plan.md
│   ├── todo.md
│   ├── work-log.md
│   └── tasks/

apps/api/README.md
apps/web/README.md
```

### Consistency Checks Required

1. **Project Structure Accuracy**
   - Directory structure references
   - File paths and locations
   - Import statements in examples
   - Command examples with correct paths

2. **API Consistency**
   - Endpoint documentation matches actual routes
   - Request/response examples are current
   - GraphQL schema documentation is accurate
   - OpenAPI spec references are valid

3. **Command Accuracy**
   - Just commands exist and work
   - Docker commands are current
   - CLI examples are valid
   - Environment setup steps work

4. **Cross-Reference Integrity**
   - Internal doc links are valid
   - Referenced sections exist
   - Navigation flows make sense
   - No orphaned documents

5. **Code Examples**
   - Import paths are correct
   - API usage examples work
   - Configuration examples are valid
   - Type definitions match code

6. **External Dependencies**
   - Package versions are current
   - External API references valid
   - Tool requirements accurate
   - System prerequisites correct

## Audit Process

### Phase 1: Catalog and Scan
1. Create inventory of all documentation
2. Extract all code examples
3. List all commands mentioned
4. Map cross-references
5. Note external dependencies

### Phase 2: Validation
1. Test all commands
2. Verify code examples compile/run
3. Check API endpoints exist
4. Validate file paths
5. Test setup procedures

### Phase 3: Analysis
1. Document all inconsistencies found
2. Categorize by severity
3. Identify root causes
4. Propose fixes

### Phase 4: Re-integration Plan
1. Group related fixes
2. Order by dependencies
3. Estimate effort
4. Create implementation plan

### Phase 5: User Review
1. Present findings summary
2. Show proposed changes
3. Get approval for plan
4. Execute approved changes

## Tools to Create

### 1. Documentation Scanner
```python
# scripts/scan-docs.py
"""Scan all documentation for consistency issues."""

def scan_file_paths(doc_content):
    """Extract and validate file paths."""
    
def scan_commands(doc_content):
    """Extract and validate commands."""
    
def scan_code_blocks(doc_content):
    """Extract and validate code examples."""
    
def scan_links(doc_content):
    """Extract and validate internal links."""
```

### 2. Consistency Report Generator
```python
# scripts/generate-consistency-report.py
"""Generate report of documentation issues."""

def generate_report(scan_results):
    """Create markdown report of findings."""
```

### 3. Documentation Test Suite
```python
# tests/test_documentation.py
"""Automated tests for documentation accuracy."""

def test_all_commands_exist():
    """Verify all documented commands work."""
    
def test_all_paths_valid():
    """Verify all documented paths exist."""
    
def test_code_examples():
    """Verify code examples are valid."""
```

## Example Inconsistencies to Look For

1. **Outdated Paths**
   - "Run `cd src && python main.py`" when it's now `apps/api/src`
   - References to old directory structure

2. **Missing Features**
   - Documented features not implemented
   - Implemented features not documented

3. **Version Mismatches**
   - Python 3.11 mentioned but using 3.12
   - Package versions outdated

4. **Broken Examples**
   - API calls with wrong parameters
   - Import statements that fail

5. **Navigation Issues**
   - Links to non-existent sections
   - Missing documentation referenced

## Definition of Done
- [ ] All documentation files scanned
- [ ] Consistency report generated
- [ ] Re-integration plan created
- [ ] `docs/workflow/normalize-docs.md` written
- [ ] Automated checks implemented
- [ ] User approval obtained
- [ ] Fixes implemented per plan
- [ ] Work log entry added