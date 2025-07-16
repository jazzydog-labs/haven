# Haven – Testing Guide

*Last updated: 2025‑07‑15*

This document explains how we keep Haven reliable by combining fast unit tests with deeper integration checks—while enforcing a **minimum 70 % coverage gate** that mirrors our CI guardrail (not currently implemented). 

---

## 1  Philosophy

* **Fail fast** – Most bugs surface at the domain layer; keep unit tests pure and in‑memory.
* **Isolate boundaries** – Integration tests run against the real Postgres and API stack to exercise adapters and routers, but using integration copies of the tables (we don't touch the real tables).
* **Measure what matters** – Coverage is a *floor*, not a goal; write meaningful assertions, not trivial line hitters.

---

## 2  Coverage Gate

Tests must satisfy **`pytest --cov=haven --cov-fail-under=70`**.  The percentage is enforced by:

* Local: `just test`
* CI / Claude Code Stop‑hook: same command; PR fails if threshold not met.

Raise the bar as the project stabilizes.

---

## 3  Directory Layout

```
tests/
├── unit/
│   ├── domain/           # pure business logic
│   └── application/
├── integration/
│   ├── api/              # HTTPX client
│   └── repository/       # real Postgres via fixtures
└── e2e/
    └── smoke_test.py     # full stack sanity check
```

Use the same package structure under `tests/` as in `src/haven/` so imports stay predictable.

---

## 4  Running the Suite

```bash
# Fast iteration (unit only)
pytest tests/unit -q

# Full battery with coverage
just test              # lint → type → pytest --cov

# Select by keyword
pytest -k "record and not slow"
```

Add `-s` to see print/debug output; add `-vv` for verbose names.

---

## 5  Common Pytest Patterns

* **Parametrization** – prefer `@pytest.mark.parametrize` over loops.
* **Monkeypatch** – stub external calls (`monkeypatch.setattr`).
* **Faker** – generate random but valid payloads (`from pytest_lazyfixture import lazy_fixture`).
* **Freezer** – pin time with `freezegun` when testing timestamps.

A sample unit test for the `Record` aggregate:

```python
@pytest.mark.parametrize("payload", ["{}", "{\"foo\": 1}"])
def test_record_payload_parses(payload):
    rec = Record.from_json(payload)
    assert rec.data is not None
```

---

## 6  Fixtures Library (`tests/conftest.py`)

| Fixture          | Scope    | Purpose                                                     |
| ---------------- | -------- | ----------------------------------------------------------- |
| `event_loop`     | session  | Asyncio loop for async tests (pytest‑asyncio)               |
| `settings`       | session  | Hydra config loaded from `conf/test`                        |
| `db_engine`      | session  | Async SQLAlchemy engine bound to a *temp* Postgres DB       |
| `alembic_runner` | session  | Applies migrations before first use                         |
| `db_session`     | function | `async_sessionmaker` yielding a rollbacked session per test |
| `client`         | function | `AsyncClient(app)` for API requests                         |

All DB fixtures rely on **test containers** started automatically by **`pytest-postgresql`**; no global state leaks.

---

## 7  Writing Integration Tests

```python
@pytest.mark.asyncio
async def test_create_record(client):
    resp = await client.post("/records", json={"data": {"hello": "world"}})
    assert resp.status_code == 201
    body = resp.json()
    assert body["data"]["hello"] == "world"
```

Behind the scenes `client` spins up the FastAPI app via Lifespan events, wires the in‑memory Hydra config, and points SQLAlchemy at the test DB fixture—you get near‑production fidelity without leaving pytest.

---

## 8  End‑to‑End Smoke Test

File: `tests/e2e/smoke_test.py`

```python
import httpx, os, pytest

BASE = os.getenv("HAVEN_BASE", "http://api.haven.local")

@pytest.mark.skipif("CI" not in os.environ, reason="run only in CI")
@pytest.mark.timeout(30)
def test_stack_healthy():
    resp = httpx.get(f"{BASE}/health")
    assert resp.status_code == 200
```

Run manually after spinning up the compose stack: `just run & pytest tests/e2e`.

---

## 9  Adding New Tests – Checklist

1. **Name** the file `test_<thing>.py`.
2. Place under `unit/` unless it hits a real DB, network, or filesystem.
3. Keep assertions focused; one concept per test.
4. Use fixtures instead of manual setup/teardown.
5. Tag slow or integration tests with `@pytest.mark.slow` so the quick path remains snappy.

---

## 10 Demos

We write an end-user demo showcasing every feature, how to integrate it in code/api, showing it off, and answering the question "why should I care?". Writing something new adds complexity, so if we don't need it we're better off not writing it. By showcasing all features in user-facing demos, we make sure that we're building something users actually care about, want, and are excited to use. Demos should be clear, to the point, and striking an excellent balance, trading off details for limited attention. We show what's most important to the user, and leave details about how to implement and integrate the SDK for that feature in the demo code itself.
---

## 11  Troubleshooting

* **DB port already in use** – run `just db-down` or kill stray containers.
* **Coverage stuck below 70 %** – use `pytest --cov --cov-report=term-missing` to see gaps.
* **Async tests hang** – ensure fixtures close connections with `await engine.dispose()`.

---

*Happy testing!*  Open an issue or drop a note in #haven-dev if you hit snags.
