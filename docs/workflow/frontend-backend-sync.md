# Frontend-Backend Synchronization Workflow

This workflow ensures the React frontend stays in sync with backend API changes through automated type generation.

## Overview

When backend models or API endpoints change, the frontend TypeScript types need to be updated to match. This workflow automates that process using OpenAPI specification generation.

## When to Use

Run the sync workflow when you:
- Add or modify domain entities
- Change API endpoints (add, remove, or modify)
- Update DTOs or response models
- Modify API request/response structures

## Quick Start

```bash
# Ensure backend is running
just docker::up-d

# Run the sync
just sync-types

# Check for breaking changes
just check-api-compat
```

## Detailed Steps

### 1. Automatic Type Generation

The `sync-types` command performs these steps:

1. **Check Backend Health** - Ensures the API is running
2. **Fetch OpenAPI Spec** - Downloads the current API specification
3. **Generate TypeScript Types** - Creates strongly-typed interfaces
4. **Format Code** - Applies prettier formatting
5. **Type Check** - Validates the generated types compile

### 2. Breaking Change Detection

The `check-api-compat` command compares the current API spec with the previous version to detect breaking changes.

### 3. Manual Review

After syncing, review the changes:

```bash
# View generated types
cat apps/web/src/types/api-generated.ts

# Check git diff
git diff apps/web/src/types/
```

## Files Generated

- `apps/web/src/types/api-generated.ts` - TypeScript interfaces for all API endpoints
- `apps/web/src/types/openapi.json` - Current OpenAPI specification
- `apps/web/src/types/openapi.prev.json` - Previous spec for comparison

## Integration with Development

### Development Workflow

1. Make backend changes
2. Run `just sync-types`
3. Fix any TypeScript errors in frontend
4. Update frontend components to use new types
5. Test the integration
6. Commit both backend and frontend changes together

### Git Hooks (Future Enhancement)

Add pre-commit hooks to remind about syncing:

```bash
#!/bin/bash
# .githooks/pre-commit
if git diff --cached --name-only | grep -q "domain/entities"; then
  echo "⚠️  Domain models changed. Remember to run: just sync-types"
fi
```

### CI/CD Integration (Future Enhancement)

Add to GitHub Actions:

```yaml
- name: Check API Compatibility
  run: |
    just docker::up-d
    just sync-types
    git diff --exit-code apps/web/src/types/
```

## Common Issues

### TypeScript Errors After Sync

If you get TypeScript errors after syncing:

1. **Naming Conflicts** - Check for type names that conflict with built-in types (e.g., `Record`)
2. **Import Paths** - Ensure imports reference the correct generated types
3. **Breaking Changes** - Backend may have introduced incompatible changes

### API Not Running

If sync fails with "Backend not running":

```bash
# Start the backend
just docker::up-d

# Wait for it to be healthy
sleep 10

# Try again
just sync-types
```

## Customization

### Modify Generation Options

Edit `scripts/sync-frontend-backend.sh` to customize:

- `--immutable` - Make all types readonly
- `--path-params-as-types` - Use template literals for path parameters
- Add `--enum` - Generate TypeScript enums instead of unions

### Generate API Client (Future)

To generate a full API client:

```bash
npx @hey-api/openapi-ts \
  -i http://api.haven.local/openapi.json \
  -o apps/web/src/services/api/generated \
  -c fetch
```

## Best Practices

1. **Regular Syncing** - Run sync after every backend API change
2. **Commit Together** - Always commit backend and frontend changes in the same commit
3. **Review Generated Code** - Check the generated types make sense
4. **Test Integration** - Ensure frontend still works after sync
5. **Document Breaking Changes** - Note any breaking API changes in commit messages

## Tools Required

- `openapi-typescript` - Generates TypeScript types from OpenAPI
- `prettier` - Formats the generated code
- `typescript` - Type checks the result

All tools are automatically installed when running `npm install` in the web directory.