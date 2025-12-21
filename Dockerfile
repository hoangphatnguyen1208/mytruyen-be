# Stage 1: Builder
FROM python:3.12-slim AS builder

# Thiết lập biến môi trường cho uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_INDEX_URL=https://download.pytorch.org/whl/cpu 

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    curl \
  && rm -rf /var/lib/apt/lists/*

# Copy uv từ image chính thức
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# 1. Copy file định nghĩa phụ thuộc
COPY pyproject.toml uv.lock ./

# 2. Cài đặt dependencies (Sử dụng --no-install-project để tách biệt layer thư viện)
# Flag --extra-index-url giúp ưu tiên bản CPU của Torch
RUN uv sync --frozen --no-cache --no-dev --extra-index-url https://download.pytorch.org/whl/cpu

# 3. Copy source code
COPY . .

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
