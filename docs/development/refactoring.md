# Haven - Refactoring Workflow Guide

*Last updated: 2025-07-16*

This guide outlines safe refactoring procedures for reorganizing directories, files, configurations, and code structure while maintaining system integrity.

---

## 1. Pre-Refactoring Checklist

Before any refactoring:

- [ ] All tests passing (`just test`)
- [ ] Clean git status (commit or stash changes)
- [ ] Document the refactoring goal
- [ ] Create a feature branch
- [ ] Backup critical configurations

---

## 2. Directory Reorganization

### Safe Move Procedure

1. **Plan the new structure**
   ```bash
   # Document current structure
   tree -d src/ > structure-before.txt
   
   # Plan new structure in a markdown file
   ```

2. **Update imports first**
   ```bash
   # Find all imports of the module
   just grep "from src.old.path import"
   
   # Use IDE refactoring tools or:
   find . -name "*.py" -exec sed -i 's/src.old.path/src.new.path/g' {} +
   ```

3. **Move files**
   ```bash
   # Create new directory structure
   mkdir -p src/new/path
   
   # Move with git to preserve history
   git mv src/old/path/*.py src/new/path/
   ```

4. **Update configuration**
   - `pyproject.toml` paths
   - `.github/workflows/` paths
   - Docker `COPY` commands
   - Documentation references

5. **Verify**
   ```bash
   just lint type test
   ```

### Common Reorganizations

#### Splitting a Large Module
```bash
# Before: src/services/everything.py (1000+ lines)
# After:  src/services/
#           ├── __init__.py
#           ├── auth.py
#           ├── data.py
#           └── utils.py
```

#### Extracting Shared Code
```bash
# Move shared utilities to common package
git mv src/api/utils.py src/common/
git mv src/graphql/utils.py src/common/
# Update imports across codebase
```

---

## 3. Configuration Refactoring

### Hydra Config Restructuring

1. **Backup current config**
   ```bash
   cp -r conf/ conf.backup/
   ```

2. **Test config composition**
   ```bash
   python -m haven.main --cfg yaml > current-config.yaml
   ```

3. **Reorganize incrementally**
   ```bash
   # Move one config group at a time
   mkdir -p conf/new_structure/
   git mv conf/old_group conf/new_structure/group
   ```

4. **Update defaults.yaml**
   ```yaml
   defaults:
     - new_structure/group: default
   ```

5. **Verify config loads**
   ```bash
   python -m haven.main --cfg yaml > new-config.yaml
   diff current-config.yaml new-config.yaml
   ```

### Environment Variable Migration

```python
# Before: Hardcoded in multiple places
DATABASE_URL = os.getenv("DB_URL", "postgresql://...")

# After: Centralized in config
# conf/database/postgres.yaml
dsn: ${oc.env:DATABASE_URL,postgresql://...}
```

---

## 4. Code Pattern Refactoring

### Extract Method
```python
# Before: Long function with multiple responsibilities
async def process_record(data: dict) -> Record:
    # 50 lines of validation
    # 30 lines of transformation  
    # 40 lines of persistence
    
# After: Extracted methods
async def process_record(data: dict) -> Record:
    validated = await validate_record_data(data)
    transformed = transform_to_entity(validated)
    return await persist_record(transformed)
```

### Replace Conditional with Polymorphism
```python
# Before: Type checking
if isinstance(processor, JsonProcessor):
    result = processor.process_json(data)
elif isinstance(processor, XmlProcessor):
    result = processor.process_xml(data)

# After: Polymorphic interface
result = processor.process(data)  # Each processor knows its format
```

---

## 5. Database Schema Refactoring

### Safe Column Rename

1. **Add new column**
   ```python
   # alembic/versions/xxx_add_new_column.py
   op.add_column('records', sa.Column('new_name', sa.String()))
   ```

2. **Copy data**
   ```python
   # alembic/versions/yyy_copy_data.py
   op.execute("UPDATE records SET new_name = old_name")
   ```

3. **Update code to use new column**
   ```python
   # Update all model references
   ```

4. **Drop old column** (after deployment)
   ```python
   # alembic/versions/zzz_drop_old_column.py
   op.drop_column('records', 'old_name')
   ```

### Table Restructuring

Always use a multi-phase approach:
1. Create new structure
2. Migrate data
3. Update code
4. Remove old structure

---

## 6. API Refactoring

### Versioning Strategy

```python
# Maintain backwards compatibility
@router.post("/api/v1/records")  # Keep old endpoint
@router.post("/api/v2/records")  # Add new endpoint
async def create_record_v2(data: RecordV2Create):
    # New implementation
```

### GraphQL Schema Evolution

```graphql
type Record {
  id: ID!
  title: String! @deprecated(reason: "Use 'name' instead")
  name: String!  # New field
}
```

---

## 7. Testing During Refactoring

### Characterization Tests
Before refactoring untested code:

```python
# Capture current behavior
def test_current_behavior():
    result = legacy_function(test_input)
    assert result == snapshot  # Capture actual output
```

### Parallel Testing
Run old and new implementations side-by-side:

```python
def test_refactored_matches_original():
    old_result = old_implementation(data)
    new_result = new_implementation(data)
    assert old_result == new_result
```

---

## 8. Rollback Procedures

### Git-based Rollback
```bash
# Tag before major refactoring
git tag pre-refactor-backup

# If needed, revert
git revert <commit-hash>
# or
git reset --hard pre-refactor-backup
```

### Feature Flag Rollback
```python
if feature_flags.use_new_implementation:
    return new_logic()
else:
    return old_logic()
```

---

## 9. Post-Refactoring Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] No performance regression
- [ ] Code coverage maintained
- [ ] API compatibility verified
- [ ] Deployment instructions updated
- [ ] Team notified of changes

---

## 10. Common Pitfalls

### Avoid These Mistakes

1. **Big Bang Refactoring** - Change everything at once
2. **No Tests** - Refactoring without test coverage  
3. **Mixed Commits** - Refactoring + features in same commit
4. **Skipping Review** - Not getting team input
5. **Breaking APIs** - Changing contracts without versioning

### Best Practices

1. **Small Steps** - Incremental changes
2. **Test First** - Ensure safety net exists
3. **Separate Commits** - Refactoring separate from features
4. **Communicate** - Keep team informed
5. **Document Why** - Record refactoring rationale

---

*Remember: The goal of refactoring is to make code better without changing behavior. Always verify behavior is preserved!*