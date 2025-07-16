# Haven – Docker Image Guide

*Last updated: 2025‑07‑16*

This document explains how we containerise Haven while keeping the final image **distroless and non‑root**.

> **Having issues?** See the [Container Troubleshooting Guide](container-troubleshooting.md) for common problems and solutions. 
---

## 1  Why Chainguard?

* **Distroless** – no shell, package manager, or glibc baggage.
* **Minimal CVE surface** – curated packages, nightly security rebuilds.
* **Multi‑arch tags** – `cgr.dev/chainguard/python` publishes both `linux/arm64` and `linux/amd64` variants.

We pin digest hashes in the Dockerfile to prevent supply‑chain surprises.

---

## 2  File Walkthrough (`Dockerfile`)

```dockerfile
# -------- Stage 1: builder -------------------------------------
FROM cgr.dev/chainguard/python:3.12-dev@sha256:<digest> AS builder

# install build deps (uv + hatch + pip cache layer)
RUN --mount=type=cache,target=/root/.cache \
    python -m pip install --upgrade pip uv hatch

WORKDIR /app

# Copy declarative deps first for cache re‑use
COPY pyproject.toml /app/
RUN uv pip install -r <(hatch dep show > /tmp/req.txt)  # resolves into /usr/local/lib/python3.12/site-packages

# Copy source last
COPY src/ /app/src
RUN hatch build -t wheel -d out

# -------- Stage 2: runtime ------------------------------------
FROM cgr.dev/chainguard/python:3.12@sha256:<digest> AS runtime
LABEL org.opencontainers.image.source="https://github.com/jazzydog-labs/haven"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/usr/local/bin:$PATH" \
    UVA_WORKERS=4

# non‑root user
USER 65532:65532

# copy wheel from builder
COPY --from=builder /app/out/*.whl /app/
RUN python -m pip install /app/*.whl && rm -rf /app

# Expose HTTP port
EXPOSE 8080

# Entrypoint via tini for signal handling
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["uvicorn", "haven.api.app:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]
```

### Key Points

1. **Cache‑friendly ordering** – deps first, code later.
2. **Non‑root UID 65532** (same as Chainguard).
3. **No shell** in runtime stage; all commands baked during build.
4. **tini** handles PID 1 signals to avoid zombie processes.

---

~~## 3  Multi‑arch Build & Push~~
Not doing this for now
---

~~## 4  SBOM & Vulnerability Scan~~
Not doing this for now
---

~~## 5  Runtime Hardening~~

* **Read‑only rootfs** – future enhancement via `COPY --from=runtime` + `RUN chmod -R 500 /usr` + `VOLUME /tmp`.
* **Drop capabilities** – add `--cap-drop ALL` in Kubernetes or `compose.yaml`.
* **Resource limits** – set `mem_limit`/`cpus` in docker‑compose; prod orchestrators should enforce.

---
Skipping
~~## 6  Development vs Production~~
Skipping for now
---

## 7  Troubleshooting

* *buildx not found* – `docker buildx install` then restart shell.
* *CVE scan fails* – check `<https://security.scw.cloud>` for patched Chainguard digest or update Python patch version.

---

For deeper Chainguard docs see [https://github.com/chainguard-images](https://github.com/chainguard-images).
