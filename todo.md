Inside `CLAUDE.md` (or a separate `guardrails/checklist.yaml`) describe “definition of done”:

- Ruff = 0 errors
    `just lint`
- Pyright strict = pass
    `just types`
- pytest cov ≥ 70 %, all tests pass
    `just test`
- MkDocs build succeeds
	- `just docs`
- demo for the feature is built showcasing high-impact features and gets "wow!" response from user, also showing how to use it
	- `just demo`
- feature is commited


I put explanations of the code in other .md files. There's architecture.md, checklist.md, (feature).md, components.md, navigation.md.

These are designed to be easy for humans to read. There's also notes on things like deprecated libs to avoid, or how to use the design system. Get it to update things as they change.

Claude.md for me is a kind of directory to tell it what to read based on what it's trying to do.

Roadmap.md is one of my favorites. A lot of the problems that arise for both human and LLM coders is that we don't notice that there's tech debt or incomplete items. It's also easy to get back into 'flow' 7 months later.




Track progress in todo.md



When resuming work:
1. Check todo.md for current progress
2. Review docs for implementation strategy (todo: add the relevant docs in here)
3. Continue from the next uncompleted task (see todo.md, commits-plan.md, and other relevant files) (todo: add relevant files here)
4. Make commits at each major milestone (as outlined in project plan)
5. Ensure tests pass before each commit as described in docs


Anything that we need to keep track of as a configuration, we should be pulling that to our config, --it should not live in .md docs, but we start with tracking it in .md docs.


Add a refactor workflow document that reorganizes the directory, files, config, etc


**TODO**: For `rest.md` and `graphql.md`, regenerate or tweak whenever the API surface changes.