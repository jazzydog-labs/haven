# Multi-stage Dockerfile for Haven
# Produces a minimal, secure production image

# Stage 1: Builder
FROM python:3.12-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /build

# Copy dependency files
COPY pyproject.toml .
COPY README.md .

# Create wheel
RUN pip install --upgrade pip build && \
    python -m build --wheel

# Stage 2: Dependencies
FROM python:3.12-slim as dependencies

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy wheel from builder
COPY --from=builder /build/dist/*.whl /tmp/

# Install application
RUN pip install --no-cache-dir /tmp/*.whl && \
    rm -rf /tmp/*

# Stage 3: Runtime
FROM python:3.12-slim

# Install only essential runtime libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    tini \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r haven && \
    useradd -r -g haven -u 1000 haven

# Copy installed packages from dependencies stage
COPY --from=dependencies /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

# Set up application directory
WORKDIR /app

# Copy application code
COPY --chown=haven:haven src ./src
COPY --chown=haven:haven conf ./conf
COPY --chown=haven:haven alembic.ini .
COPY --chown=haven:haven alembic ./alembic

# Create necessary directories
RUN mkdir -p /app/logs && chown -R haven:haven /app

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.local/bin:$PATH" \
    PYTHONPATH=/app/src

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Switch to non-root user
USER haven

# Expose port
EXPOSE 8080

# Use tini as entrypoint for proper signal handling
ENTRYPOINT ["tini", "--"]

# Run the application
CMD ["python", "-m", "haven.main"]