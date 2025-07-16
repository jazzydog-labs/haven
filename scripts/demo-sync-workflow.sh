#!/bin/bash
# Demo script for Frontend-Backend Sync Workflow

set -e

echo "🎬 Frontend-Backend Sync Workflow Demo"
echo "====================================="
echo ""

# 1. Check if backend is running
echo "1️⃣ Checking backend status..."
if curl -s http://localhost:8080/health > /dev/null 2>&1; then
  echo "✅ Backend is running"
else
  echo "❌ Backend not running. Please start with: just run-docker-d"
  exit 1
fi

# 2. Show current types
echo ""
echo "2️⃣ Current types structure..."
if [ -f apps/web/src/types/api-generated.ts ]; then
  echo "📄 Generated types exist:"
  wc -l apps/web/src/types/api-generated.ts
else
  echo "📄 No generated types yet"
fi

# 3. Run sync
echo ""
echo "3️⃣ Running type synchronization..."
echo ""
./scripts/sync-frontend-backend.sh

# 4. Show what changed
echo ""
echo "4️⃣ Changes detected:"
if [ -f apps/web/src/types/openapi.prev.json ]; then
  echo "📊 API spec differences:"
  diff -u apps/web/src/types/openapi.prev.json apps/web/src/types/openapi.json | head -20 || echo "No changes"
else
  echo "📊 First time sync - no previous spec to compare"
fi

# 5. Show generated types
echo ""
echo "5️⃣ Generated TypeScript types preview:"
echo "-------------------------------------"
head -50 apps/web/src/types/api-generated.ts | grep -E "(interface|type|export)" || echo "No types generated"

# 6. Available commands
echo ""
echo "6️⃣ Available sync commands:"
echo "  • just sync-types       - Sync frontend types with backend"
echo "  • just check-api-compat - Check for breaking API changes"
echo "  • just generate-frontend-crud <model> - Generate CRUD components (TODO)"

echo ""
echo "✨ Demo complete! The frontend types are now synchronized with the backend API."
echo ""
echo "Next steps:"
echo "1. Review generated types in apps/web/src/types/api-generated.ts"
echo "2. Update frontend components to use the new types"
echo "3. Run 'npm test' to ensure everything works"