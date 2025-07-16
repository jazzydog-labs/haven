# Haven – Code‑Quality Guide

*Last updated: 2025‑07‑15*

This page documents the linting, formatting, and static‑type requirements that every Haven contribution must satisfy before merge.  All commands run locally via **Justfile** targets and are mirrored in our automation guardrails so the same rules apply everywhere.

---

## 1  Philosophy

* **Fail early, fail fast** – surface issues at commit time, not in code review.
* **Single source of truth** – Ruff handles both *lint* and *format*; Pyright enforces types.
* **Zero‑noise policy** – the default branch must be *green* (0 Ruff violations, 0 Pyright errors). Any new warnings block merge.

---

## 2  Ruff – Linter + Formatter

### 2.1  Why Ruff?

* Blazing speed (Rust implementation).
* Superset of Flake8 rules plus auto‑formatter (`ruff format`).
* Extensible yet defaults cover 90 % of Python style guides.

### 2.2  Configuration (in **pyproject.toml**)

```toml
[tool.ruff]
# Enable common rule bundles
select = [
  "E",   # Pycodestyle errors
  "F",   # Pyflakes
  "I",   # Import order
  "B",   # Bugbear
  "UP",  # PyUpgrade
  "C4",  # Comprehension hygiene
  "SIM", # Simplifications
]
# Project‑specific ignores (example)
ignore = ["D100", "D104"]  # Missing module/docstring warnings in tests

# Treat warnings as errors during CI (via --exit‑non‑zero‑on‑warn)
unsafe‑fixes = false

# Enable Ruff formatter
[tool.ruff.format]
preview = true
line‑length = 100
```

### 2.3  Running Ruff

```bash
just lint            # ruff check .
just lint‑fix        # ruff check --fix . && ruff format .
```

Both commands run inside the Hatch virtual‑env—no global installs required.

---

## 3  Pyright – Static Type Checking

### 3.1  Why Pyright?

* Fast incremental analysis.
* **Strict** mode catches nullable mistakes, implicit `Any`, etc.
* Works out‑of‑the‑box with Pydantic v2 models (via `from __future__ import annotations`).

### 3.2  Configuration (**pyrightconfig.json** at repo root)

```json
{
  "typeCheckingMode": "strict",
  "pythonVersion": "3.12",
  "reportMissingImports": true,
  "reportMissingTypeStubs": false,
  "exclude": [".venv", "**/migrations"]
}
```

> **Note:** We omit test folders from `exclude` so parameterized test functions stay type‑checked.

### 3.3  Running Pyright

```bash
just type           # pyright
```

Pyright strictness cannot be silenced by noqa; fix the type error or add an explicit ignore comment if unavoidable.

---

## 4  Pre‑commit Hooks

We ship a **.pre‑commit‑config.yaml** to automate quality gates before every commit:

```yaml
repos:
  - repo: https://github.com/astral‑sh/ruff
    rev: v0.4.6
    hooks:
      - id: ruff
        args: ["check", "--fix"]
      - id: ruff‑format
  - repo: https://github.com/microsoft/pyright
    rev: v1.1.361
    hooks:
      - id: pyright
        additional_dependencies: []
```

Install once per clone:

```bash
pre‑commit install
```

Now `git commit` will block until Ruff and Pyright pass—mirroring **just lint type**.

---

## 5  Integration with Justfile

```text
lint        – ruff check .
lint‑fix    – ruff check --fix . && ruff format .
type        – pyright
lint type   – ruff then pyright
```

Add more combos (e.g., `lint type test`) as aliases; Justfile is the canonical task runner for everybody and for Claude Code’s hooks.

---

## 6  CI & Claude Guardrails

* The **Stop hook** (`just lint type test`) ensures both tools are executed after every automated code change.
* CI scripts and local `just test` both run `ruff --exit‑non‑zero‑on‑warn` so warnings fail builds.
* Coverage gate is handled separately (see `testing.md`).

---

## 7  Definition of Done

All code must meet these quality gates before being considered complete:

1. **Linting**: `just lint` - 0 errors, 0 warnings
2. **Type Check**: `just type` - All checks pass in strict mode  
3. **Tests**: `just test` - All pass with ≥70% coverage
4. **Docs Build**: `just docs` - Builds without errors
5. **Demo**: Feature demonstrated with clear value proposition
6. **Committed**: Changes are committed with clear message

See `docs/definition-of-done.md` for the complete checklist.

---

## 8  Troubleshooting

| Symptom                             | Fix                                                                                          |
| ----------------------------------- | -------------------------------------------------------------------------------------------- |
| Ruff ignores config                 | Ensure `[tool.ruff]` lives in **pyproject.toml**; run `ruff linter‑info`.                    |
| Pyright flags Pydantic model fields | Add `model_config = ConfigDict(arbitrary_types_allowed=True)` or annotate fields explicitly. |
| VS Code shows different errors      | Install the “Pyright” extension and point it at `pyrightconfig.json`.                        |

---

*Questions? Open a discussion thread or ping #haven‑dev.*
