### Haven — Documentation Map (non-table edition)

Below is a narrative “sitemap” of every document we plan to maintain, where it will live, and what it’s for.  

---

#### 1 Project Entry Points – repo root

- **`README.md`**
    
    - _Why it exists_: the one-screen elevator pitch and quick-start.
        
    - _What goes inside_: purpose, install snippet (`just install`), how to run, badge links, pointer to full docs.
        
    - _When to update_: every release or whenever onboarding steps change.
        
- **`CLAUDE.md`**
    
    - _Why_: living changelog + design-decision diary.
        
    - _What_: incremental progress notes, tick-box TODOs, links to new docs.
        
    - _When_: after each meaningful commit.
        

---

#### 2 Core Specs & Planning – `docs/`

- **`spec.md`**
    
    - _Why_: immutable North Star—goals, tech choices, success criteria.
        
    - _When_: only on scope shifts.
        
- **`commits_plan.md`**
    
    - _Why_: storyboard of intended milestones.
        
    - _When_: rarely—if roadmap moves.
        
- **`architecture.md`**
    
    - _Why_: diagrams and narrative about layers, dependencies, sequence flows.
        
    - _When_: anytime the architecture evolves.
        
- **`roadmap.md`**
    
    - _Why_: tracks planned features, technical debt, and incomplete items to maintain development flow.
        
    - _When_: weekly updates on progress, new items as discovered.
        
- **`definition-of-done.md`**
    
    - _Why_: clear checklist ensuring all code meets quality standards before merge.
        
    - _When_: rarely—only if team agrees on new criteria.

---

#### 3 Developer How-Tos – `docs/setup` and friends

- **`setup/local_dev.md`** – environment setup, Docker compose, Justfile cheat-sheet.
    
- **`testing.md`** – pytest patterns, coverage gate, fixtures.
    
- **`quality.md`** – Ruff & Pyright rules, pre-commit info.
    
- **`configuration.md`** – Hydra tree explained, env overrides.
    
- **`database/alembic.md`** – migration workflow, branching, squash policy.
    
- **`refactoring.md`** – safe procedures for reorganizing code, directories, and configurations.
    

_Update these whenever corresponding tooling or process changes._

---

#### 4 API References – `docs/api/`

- **`api/rest.md`** – endpoint list with example requests/responses.
    
- **`api/graphql.md`** – SDL, sample queries/mutations, pagination examples.
    

_Regenerate or tweak whenever the surface changes._

---

#### 5 Operations & Deployment – `docs/deploy/`

- **`docker.md`** – multi-stage Dockerfile walkthrough, hardening notes.
    
~~- **`compose.md`** – service stack, volumes, local vs. CI overrides.~~
    
~~- **`release.md`** – manual release checklist (tag, smoke test, doc publish).~~
    

_Revise when deployment mechanics evolve._

---

#### 6 MkDocs Site Structure

Everything under `docs/` is automatically rendered by MkDocs-Material.  
Top-level navigation is controlled by `mkdocs.yml`; rebuilding is as simple as `just docs`.

**Note**: MkDocs configuration and theme setup to be implemented in a future commit.

---

#### 7 Community & Future 

These documents will be added as the project matures:

- **`glossary.md`** – definitions of key terms (Record, UoW, etc.).
- **`contributing.md`** – PR etiquette, code-review checklist.
- **`changelog.md`** – user-facing changes per release.

_Update these continuously as norms and ambitions grow._

---

#### 8 Non-Prose Configuration Artifacts

Files like `pyproject.toml`, `.justfile`, `mkdocs.yml`, and `alembic.ini` live at the repo root. They’re referenced from the guides above but are not documentation themselves.

---

### Using this Map

1. Add it to the docs directory and link it first in `mkdocs.yml`.
    
2. Treat it as a living index—every time you add or rename a doc, come back here.
    
3. New contributors can read this single page and know exactly where to dive in.