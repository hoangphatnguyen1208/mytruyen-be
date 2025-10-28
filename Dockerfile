# Multi-stage build for a small production image
FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    curl \
  && rm -rf /var/lib/apt/lists/*

COPY . ./app

WORKDIR /app
RUN uv sync --frozen --no-cache

# Production image
FROM python:3.12-slim

# Tạo user không có quyền root để tăng bảo mật
RUN groupadd -g 1001 app && \
    useradd -u 1001 -g app -m -d /app -s /usr/sbin/nologin app

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép ứng dụng và virtual environment từ builder
COPY --from=builder --chown=app:app /app /app

# Thêm thư mục .venv vào PATH để lệnh "uv" hoặc "fastapi" có thể chạy trực tiếp
ENV PATH="/app/.venv/bin:$PATH"

# Mở cổng chạy app (ví dụ FastAPI)
EXPOSE 8000

# Chuyển sang user không phải root
USER app
