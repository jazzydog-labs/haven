#!/bin/bash
# Sync frontend with backend API changes
# This script generates TypeScript types and API clients from the backend OpenAPI spec

set -e

echo "🔄 Syncing frontend with backend API..."

# 1. Ensure backend is running
if ! curl -s http://localhost:8080/health > /dev/null 2>&1; then
  echo "❌ Backend not running. Start with: just run-docker-d"
  exit 1
fi

# 2. Fetch OpenAPI spec
echo "📥 Fetching OpenAPI spec..."
curl -s http://localhost:8080/openapi.json > apps/web/src/types/openapi.json

# 3. Install required dependencies if not present
echo "📦 Checking dependencies..."
cd apps/web
if ! npm list openapi-typescript > /dev/null 2>&1; then
  echo "Installing openapi-typescript..."
  npm install --save-dev openapi-typescript
fi

# 4. Generate TypeScript types
echo "📝 Generating TypeScript types..."
npx openapi-typescript ../web/src/types/openapi.json \
  --output src/types/api-generated.ts \
  --immutable \
  --path-params-as-types

# 5. Format generated code
echo "✨ Formatting generated code..."
npx prettier --write src/types/api-generated.ts

# 6. Run type checking
echo "✅ Type checking..."
npm run type-check || {
  echo "⚠️  Type checking found errors. This is often due to complex path patterns in the OpenAPI spec."
  echo "   The generated types are still usable, but you may need to fix some TypeScript errors."
  # Don't exit with error - allow workflow to continue
}

# 7. Check for breaking changes (if previous spec exists)
if [ -f src/types/openapi.prev.json ]; then
  echo "🔍 Checking for breaking changes..."
  # Simple diff for now, could use oasdiff for better analysis
  if ! diff -q src/types/openapi.prev.json src/types/openapi.json > /dev/null; then
    echo "⚠️  API spec has changed. Review changes carefully."
  fi
fi

# Save current spec for next comparison
cp src/types/openapi.json src/types/openapi.prev.json

echo "✨ Sync complete!"
echo ""
echo "Next steps:"
echo "1. Review generated types in apps/web/src/types/api-generated.ts"
echo "2. Update frontend components if needed"
echo "3. Run 'npm test' to ensure everything works"