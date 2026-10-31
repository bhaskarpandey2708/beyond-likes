# Beyond Likes Discourse Intelligence Platform
# Production Multi-Stage Container Image
FROM python:3.12-slim AS builder

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install uv for blazingly fast dependency installation
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy configuration and dependency specs
COPY . /app

# Create virtual environment and install dependencies
RUN uv venv /app/.venv && \
    uv pip install --python /app/.venv/bin/python --extra-index-url https://download.pytorch.org/whl/cpu \
    torch transformers sentencepiece protobuf tiktoken onnx onnxruntime

# Final Runtime Image
FROM python:3.12-slim AS runner

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

COPY --from=builder /app /app

EXPOSE 8888

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8888/v1/health || exit 1

CMD ["python3", "api/server.py"]
