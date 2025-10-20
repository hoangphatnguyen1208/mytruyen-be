# Multi-stage build for a small production image
FROM python:3.12-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    curl \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only dependency spec to leverage Docker cache
COPY pyproject.toml pyproject.toml
COPY README.md README.md

# Install pip and wheel
RUN python -m pip install --upgrade pip setuptools wheel

# Install runtime dependencies
RUN pip install \
    "alembic>=1.16.5" \
    "asyncpg>=0.30.0" \
    "bcrypt>=4.3.0" \
    "fastapi[standard]>=0.116.1" \
    "passlib>=1.7.4" \
    "psycopg2-binary>=2.9.10" \
    "pydantic-settings>=2.10.1" \
    "pyjwt>=2.10.1" \
    "sqlmodel>=0.0.25"

# Production image
FROM python:3.12-slim
LABEL maintainer=""

ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PATH="/home/app/.local/bin:$PATH"

# Create app user
RUN addgroup --system app && adduser --system --ingroup app app

WORKDIR /app

# Copy installed packages from builder is not trivial; instead install again (small overhead)
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy project
COPY . /app

# Expose port
EXPOSE 8000

# Run as non-root
USER app




