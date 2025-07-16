# Tasks Workflow

## Overview

The tasks workflow helps manage feature requests, bugs, and improvements through a structured lifecycle from conception to completion.

## Directory Structure

```
tasks/
├── open/     # Active tasks waiting to be implemented
└── closed/   # Completed tasks for archival
```

## Task Lifecycle

### 1. Creating a Task

Create a new markdown file in `tasks/open/` with a descriptive filename:

```bash
# Example filenames
tasks/open/user-authentication.md
tasks/open/graphql-pagination.md
tasks/open/database-connection-pooling.md
```

### 2. Task File Format

Each task file should contain:

```markdown
# Task: [Brief Title]

## Description
Clear description of what needs to be implemented.

## Acceptance Criteria
- [ ] Specific requirement 1
- [ ] Specific requirement 2
- [ ] Specific requirement 3

## Implementation Notes
- Technical considerations
- Dependencies
- Potential challenges

## Definition of Done
- [ ] Feature implemented
- [ ] Tests added
- [ ] Documentation updated
- [ ] Code reviewed
```

### 3. Planning Phase

When ready to implement a task:

1. **Add to Roadmap**: Reference the task in `docs/roadmap.md`
   ```markdown
   ## Next Sprint
   - Implement user authentication (see `tasks/open/user-authentication.md`)
   ```

2. **Add to Commits Plan**: Break down into commits in `docs/commits-plan.md`
   ```markdown
   ### Phase 2: Authentication (3 commits)
   - commit 4: Add user model and repository
   - commit 5: Implement JWT authentication
   - commit 6: Add login/logout endpoints
   
   Reference: `tasks/open/user-authentication.md`
   ```

### 4. Implementation

During implementation:
- Follow the commits plan
- Update progress in work log
- Check off acceptance criteria as completed

### 5. Task Completion

When task is fully complete:

1. **Move to closed**: `mv tasks/open/task-name.md tasks/closed/`
2. **Update final status**: Add completion date and summary
3. **Update roadmap**: Mark as completed
4. **Clean up commits plan**: Archive completed sections

## Referencing Tasks

Tasks can be referenced by filename from any documentation:

- `docs/roadmap.md`: "Implement GraphQL subscriptions (see `graphql-subscriptions.md`)"
- `docs/commits-plan.md`: "Reference: `tasks/closed/basic-crud-operations.md`"
- `work-log.md`: "Completed task defined in `user-authentication.md`"

## Benefits

- **Traceability**: Clear link from idea to implementation to completion
- **Planning**: Tasks inform roadmap and commit planning
- **History**: Closed tasks provide implementation context
- **Reusability**: Similar tasks can reference previous implementations

## Commands

```bash
# Create new task
touch tasks/open/new-feature.md

# List open tasks
ls tasks/open/

# Move completed task
mv tasks/open/completed-task.md tasks/closed/

# Search tasks
grep -r "authentication" tasks/
```

## Integration with Development Workflow

This tasks workflow integrates with the existing development cycle:

1. **Task Creation** → Add to `tasks/open/`
2. **Planning** → Reference in roadmap and commits plan  
3. **Implementation** → Follow standard dev workflow from CLAUDE.md
4. **Completion** → Move to `tasks/closed/` and update logs

Tasks provide the "what to build" while the existing workflow handles "how to build it".