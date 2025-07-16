# Multi-stage Dockerfile for Haven API
# Development-focused with hot-reload support

# Stage 1: Base
FROM python:3.12-slim as base

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: Development
FROM base as development

# Install build dependencies for development
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r haven && \
    useradd -r -g haven -u 1000 haven

# Set working directory
WORKDIR /app

# Copy dependency files
COPY --chown=haven:haven pyproject.toml ./
COPY --chown=haven:haven README.md ./

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -e ".[dev]"

# Copy application code (in dev, this will be overridden by volume mount)
COPY --chown=haven:haven src ./src
COPY --chown=haven:haven conf ./conf
COPY --chown=haven:haven alembic.ini ./
COPY --chown=haven:haven alembic ./alembic

# Create necessary directories
RUN mkdir -p /app/logs && chown -R haven:haven /app

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src \
    HYDRA_FULL_ERROR=1

# Switch to non-root user
USER haven

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run with hot-reload enabled
CMD ["python", "-m", "haven.main"]

# Stage 3: Production (for future use)
FROM base as production

# Copy built wheel from builder stage (to be implemented)
# This stage would use the multi-stage build pattern from the original Dockerfile

# For now, we focus on development stage