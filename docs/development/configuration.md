# Haven – Configuration Guide (Hydra)

*Last updated: 2025-07-15*

Haven relies on **Hydra 1.3** for hierarchical, environment‑aware configuration.  This guide explains the directory layout, how overrides work, and where environment variables fit in.  After reading you should be able to:

* Spin up Haven with a custom database URL in one command.
* Add a new config group (e.g., `cache/redis.yaml`).
* Understand where secrets live and how they’re injected.

---

## 1  Directory Layout

```
conf/
├── defaults.yaml          # global include list (ordered)
├── environment/
│   ├── local.yaml         # developer laptop defaults
│   ├── test.yaml          # CI / pytest overrides
│   └── prod.yaml          # production‑ish example
├── database/
│   ├── postgres.yaml      # default Postgres 16 settings
│   └── sqlite.yaml        # in‑memory option for unit tests
├── logging/
│   └── default.yaml       # structured JSON logging
└── model/
    └── record.yaml        # future model‑specific knobs
```

> **defaults.yaml** is Hydra’s “root” that tells it which configs to merge by default:
>
> ```yaml
> defaults:
>   - environment: local
>   - database: postgres
>   - logging: default
> ```

When you run Haven without arguments, Hydra composes `environment/local`, `database/postgres`, and `logging/default`.

---

## 2  Config Object Lifecycle

1. **Hydra** parses YAML files, applies CLI overrides, then hands the dict to…
2. **Pydantic Settings class** (`haven.config.settings.AppSettings`) which casts fields, validates types, and performs interpolation (e.g., `${oc.env:DATABASE_URL}` falls back to env var).
3. The validated object is injected into FastAPI via dependency (`Depends(get_settings)`).

Any invalid value aborts startup with a clear error message.

---

## 3  Environment Variables

Each YAML field can reference an env var using `${oc.env:VAR_NAME}`.  Example in `database/postgres.yaml`:

```yaml
dsn: ${oc.env:DATABASE_URL,postgresql+asyncpg://haven:haven@localhost:5432/haven}
```

* If `$DATABASE_URL` is set, it wins.
* Otherwise the default DSN points at the local compose stack.

Secrets like passwords **must** come from env vars; do not commit them to YAML.

---

## 4  Common Override Scenarios

### 4.1  Switch environment

```bash
python -m haven.main +environment=test          # uses environment/test.yaml
```

### 4.2  Swap database backend

```bash
python -m haven.main +database=sqlite
```

### 4.3  Ad‑hoc value change

```bash
python -m haven.main database.port=5544
```

Hydra merges overrides from left to right, so later arguments win.

---

## 5  Using `.env` Files

We ship a template at `conf/local/.env.example`.  Copy to project root and source it:

```bash
cp conf/local/.env.example .env
export $(grep -v '^#' .env | xargs)
```

Python‑dotenv auto‑loads the file during app startup, so you rarely need to `export` manually.

---

## 6  Adding a New Config Group

1. Create the folder, e.g., `cache/`.
2. Add YAML file(s): `redis.yaml`, `local.yaml` …
3. Update `defaults.yaml` with `- cache: redis` if it should load by default.
4. Extend `AppSettings` with a new nested Pydantic model: `CacheSettings`.

Hydra will merge it automatically.

---

## 7  Runtime Introspection

At any time you can dump the composed config:

```bash
python -m haven.main --cfg pretty
```

Hydra prints the final YAML so you can confirm overrides.

---

## 8  Tips & Caveats

* **Order matters** – defaults apply top‑down; list more specific configs last.
* **No secrets in git** – use env vars or a secrets manager.
* **Validate early** – keep as much validation in Pydantic models as possible.
* **CI** uses `environment=test` and `database=postgres` but points `DATABASE_URL` at the containerized Postgres.

---

## 9  Troubleshooting

* *ValueError on startup* – run with `HYDRA_FULL_ERROR=1` to see stack trace.
* *Env var not picked up* – verify it’s exported in the same shell; use `printenv DATABASE_URL`.
* *Unexpected config key* – Pydantic will raise; check spelling or update model.

---

*For deeper Hydra magic, see [https://hydra.cc/docs/intro/](https://hydra.cc/docs/intro/).*
