#!/bin/bash
# Version bump script for Haven

set -euo pipefail

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Current version
CURRENT_VERSION=$(grep '^version = ' pyproject.toml | cut -d'"' -f2)

# Parse arguments
BUMP_TYPE="${1:-patch}"

# Function to bump version
bump_version() {
    local version=$1
    local type=$2
    
    IFS='.' read -r major minor patch <<< "$version"
    
    case $type in
        major)
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        minor)
            minor=$((minor + 1))
            patch=0
            ;;
        patch)
            patch=$((patch + 1))
            ;;
        *)
            echo -e "${RED}Invalid bump type: $type${NC}"
            echo "Usage: $0 [major|minor|patch]"
            exit 1
            ;;
    esac
    
    echo "$major.$minor.$patch"
}

# Calculate new version
NEW_VERSION=$(bump_version "$CURRENT_VERSION" "$BUMP_TYPE")

echo -e "${GREEN}Bumping version from $CURRENT_VERSION to $NEW_VERSION${NC}"

# Update pyproject.toml
sed -i.bak "s/^version = \".*\"/version = \"$NEW_VERSION\"/" pyproject.toml
rm pyproject.toml.bak

# Update __init__.py
sed -i.bak "s/__version__ = \".*\"/__version__ = \"$NEW_VERSION\"/" src/haven/__init__.py
rm src/haven/__init__.py.bak

# Update conf files
find conf -name "*.yaml" -type f -exec sed -i.bak "s/version: .*/version: $NEW_VERSION/" {} \;
find conf -name "*.yaml.bak" -type f -delete

echo -e "${GREEN}Version bumped to $NEW_VERSION${NC}"
echo "Don't forget to:"
echo "  1. Update CHANGELOG.md"
echo "  2. Commit changes"
echo "  3. Tag the release: git tag -a v$NEW_VERSION -m 'Release v$NEW_VERSION'"