# Task: Reorganize Project Documentation and Configuration Structure

## Description
Audit and reorganize the entire project structure (excluding src/ code directories) to ensure documentation, configuration files, and other project assets are logically organized and easy to navigate. Create a clear, intuitive directory structure that follows best practices and makes it easy for developers to find what they need.

## Acceptance Criteria
- [ ] Audit current project root and docs structure
- [ ] Design new logical directory structure for non-code files
- [ ] Move files to appropriate locations with consistent naming
- [ ] Update all internal references and imports after moves
- [ ] Create directory README files where helpful for navigation
- [ ] Update CLAUDE.md to reflect new structure
- [ ] Ensure CI/CD and tooling still work after reorganization
- [ ] Verify all documentation links are updated

## Current Structure Issues to Address
- Mixed configuration files in root directory
- Documentation scattered across different locations
- Task management files not clearly organized
- Build and deployment configs need better grouping
- Example/demo files location unclear

## Proposed Structure Categories

### Documentation Organization
```
docs/
├── architecture/          # Architecture decisions and patterns
├── development/          # Developer guides and workflows  
├── operations/           # Deployment, monitoring, maintenance
├── api/                  # API documentation and examples
└── project-management/   # Planning, tasks, tracking
```

### Configuration Management
```
config/
├── development/          # Dev-specific configs
├── production/          # Prod configs
├── ci-cd/               # Build and deployment configs
└── tools/               # Linting, formatting, etc.
```

### Project Assets
```
scripts/                 # Build, deployment, utility scripts
examples/               # Sample code and demos
templates/              # File templates and scaffolding
```

## Implementation Notes
- Preserve git history during file moves using `git mv`
- Update justfile paths and imports
- Check for hardcoded paths in documentation
- Consider creating index files for major directories
- Maintain backward compatibility where possible
- Update .gitignore if directory structure changes

## Cross-References to Update
- CLAUDE.md documentation map
- All justfile references
- CI/CD pipeline configurations
- Import statements in configuration files
- Internal documentation links

## Definition of Done
- [ ] All non-code files are in logical, consistent locations
- [ ] Directory structure follows clear categorization principles
- [ ] All internal references and links are updated and working
- [ ] CLAUDE.md reflects the new structure accurately
- [ ] CI/CD pipelines execute successfully
- [ ] All existing functionality works without breaking changes
- [ ] New structure is documented with clear navigation guidance
- [ ] Team can easily locate files and understand organization principles