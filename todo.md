[DONE] Definition of done has been documented in `docs/definition-of-done.md` with complete checklist:

- Ruff = 0 errors (`just lint`)
- Pyright strict = pass (`just type`) 
- pytest cov ≥ 70%, all tests pass (`just test`)
- MkDocs build succeeds (`just docs`)
- Demo showcasing high-impact features (`just demo`)
- Feature is committed with clear message

See also: `docs/quality.md` for detailed quality gate information.


[DONE] Documentation structure has been established:

- `docs/architecture.md` - Clean Architecture patterns and layer design
- `docs/definition-of-done.md` - Complete quality checklist
- `docs/roadmap.md` - Feature planning and technical debt tracking
- `docs/refactoring.md` - Safe code reorganization procedures
- Additional feature-specific docs to be added as features are implemented

CLAUDE.md now serves as a directory pointing to relevant documentation based on the task at hand.

The roadmap.md is particularly useful for tracking tech debt and maintaining development flow across sessions.




[IN PROGRESS] Track progress across multiple documents:
- This file (todo.md) - Immediate tasks and notes
- `docs/roadmap.md` - Long-term planning and tech debt
- `docs/commits-plan.md` - Implementation milestones



When resuming work:
1. Check `todo.md` for immediate tasks
2. Review docs for implementation strategy:
   - `docs/roadmap.md` - Current sprint and backlog
   - `docs/commits-plan.md` - Implementation order
   - `docs/architecture.md` - Design patterns to follow
   - `CLAUDE.md` - Quick reference and doc directory
3. Continue from the next uncompleted task
4. **Complete the task fully**
5. Ensure all quality gates pass (see `docs/definition-of-done.md`)
6. **Commit immediately with clear message**
7. Move to the next task

**Critical**: Never batch multiple tasks into one commit. Each logical unit of work should be committed separately for clear history and safe rollbacks.


[NOTE] Configuration management principle:
- Start by documenting configs in .md files for visibility
- Once stable, migrate to proper config files (Hydra yaml, pyproject.toml, etc.)
- Config should live in code, not documentation
- See `docs/configuration.md` for Hydra config management


[DONE] Refactoring workflow documented in `docs/refactoring.md`:
- Safe procedures for directory reorganization
- Config migration strategies  
- Code pattern refactoring
- Database schema evolution
- Rollback procedures


[DONE] API documentation created:
- `docs/api/rest.md` - REST endpoint reference with examples
- `docs/api/graphql.md` - GraphQL schema and query examples

**TODO**: Set up auto-generation from OpenAPI/GraphQL schemas in future commit.