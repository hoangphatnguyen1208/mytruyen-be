# Multi-stage build for a small production image
FROM python:3.12-slim AS builder


COPY --from=ghcr.io/astral-sh/uv:0.9.5 /uv /uvx /bin/
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Dependency installation
COPY uv.lock pyproject.toml ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-install-project --no-dev

# Project installation
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev
# Production image
FROM python:3.12-slim

ENV PATH="/app/.venv/bin:$PATH"
RUN groupadd -g 1001 app && \
    useradd -u 1001 -g app -m -d /app -s /bin/false app

WORKDIR /app

COPY --from=builder --chown=app:app /app .

# Expose port
EXPOSE 8000

# Run as non-root
USER app


