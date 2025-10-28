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
RUN pip install uv \
    && uv sync --system
    

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




