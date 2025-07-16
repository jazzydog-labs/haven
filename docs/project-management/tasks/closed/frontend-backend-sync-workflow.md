# Frontend-Backend Synchronization Workflow

## Description
Establish a recurring workflow to keep the React frontend in sync with backend API changes. This ensures that when domain models or APIs are updated, the frontend is systematically updated to match.

## Acceptance Criteria
- [ ] Automated TypeScript type generation from backend models
- [ ] API client generation from OpenAPI/Swagger spec
- [ ] Change detection workflow for breaking changes
- [ ] Documentation for the sync process
- [ ] Integration with CI/CD pipeline

## Implementation Notes

### 1. TypeScript Type Generation
```bash
# Generate types from OpenAPI spec
npx openapi-typescript http://api.haven.local/openapi.json \
  --output apps/web/src/types/api-generated.ts

# Or from Python models using datamodel-code-generator
datamodel-codegen --input apps/api/src/haven/domain/entities \
  --output apps/web/src/types/domain.ts \
  --output-model-type typescript
```

### 2. API Client Generation
```bash
# Generate API client from OpenAPI
npx openapi-generator-cli generate \
  -i http://api.haven.local/openapi.json \
  -g typescript-fetch \
  -o apps/web/src/services/api/generated
```

### 3. Sync Workflow Script
```bash
#!/bin/bash
# scripts/sync-frontend-backend.sh

echo "🔄 Syncing frontend with backend API..."

# 1. Ensure backend is running
if ! curl -s http://api.haven.local/health > /dev/null; then
  echo "❌ Backend not running. Start with: just run-api"
  exit 1
fi

# 2. Generate TypeScript types
echo "📝 Generating TypeScript types..."
npx openapi-typescript http://api.haven.local/openapi.json \
  --output apps/web/src/types/api-generated.ts

# 3. Generate API client
echo "🔧 Generating API client..."
npx openapi-generator-cli generate \
  -i http://api.haven.local/openapi.json \
  -g typescript-fetch \
  -o apps/web/src/services/api/generated \
  --additional-properties=supportsES6=true,npmVersion=10.0.0

# 4. Run type checking
echo "✅ Type checking..."
cd apps/web && npm run type-check

# 5. Run tests
echo "🧪 Running frontend tests..."
npm test

echo "✨ Sync complete!"
```

### 4. Breaking Change Detection
```yaml
# .github/workflows/api-compatibility.yml
name: API Compatibility Check

on:
  pull_request:
    paths:
      - 'apps/api/src/haven/interface/**'
      - 'apps/api/src/haven/domain/**'

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Check OpenAPI compatibility
        uses: oasdiff/oasdiff-action@v0.0.17
        with:
          base: origin/main
          revision: HEAD
          fail-on: breaking
```

### 5. Just Commands
```makefile
# Add to Justfile

# Sync frontend types with backend
sync-types:
    @echo "Syncing frontend types with backend..."
    ./scripts/sync-frontend-backend.sh

# Check for API breaking changes
check-api-compat:
    oasdiff diff http://api.haven.local/openapi.json \
      <(git show main:apps/api/openapi.json) \
      --fail-on breaking

# Generate frontend from backend
generate-frontend-crud model:
    @echo "Generating CRUD components for {{ model }}..."
    ./scripts/generate-crud.sh {{ model }}
```

### 6. Git Hooks
```bash
# .githooks/pre-commit
#!/bin/bash
# Check if backend models changed
if git diff --cached --name-only | grep -q "domain/entities"; then
  echo "⚠️  Domain models changed. Remember to run: just sync-types"
fi

# Check if API routes changed  
if git diff --cached --name-only | grep -q "interface/api"; then
  echo "⚠️  API routes changed. Remember to run: just sync-types"
fi
```

### 7. Development Guidelines
```markdown
## When to Sync

Run `just sync-types` when you:
- Add/modify domain entities
- Change API endpoints
- Update DTOs
- Modify API responses

## Workflow

1. Make backend changes
2. Run `just sync-types`
3. Fix any TypeScript errors
4. Update frontend components
5. Test end-to-end
6. Commit both backend and frontend changes together
```

## Tools Required
- openapi-typescript
- openapi-generator-cli
- oasdiff (for breaking change detection)
- datamodel-code-generator (optional)

## Definition of Done
- [ ] Type generation script working
- [ ] API client generation working
- [ ] Just commands added
- [ ] CI/CD integration for compatibility checks
- [ ] Git hooks for reminders
- [ ] Team documentation and training
- [ ] Work log entry added