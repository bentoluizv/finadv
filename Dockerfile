FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

# Compile bytecode for faster startup; copy files instead of hardlinks
# (required when cache and project are on different filesystems in Docker)
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app

# Install dependencies first — this layer is cached as long as the lockfile
# does not change, even when source code changes.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

# Copy the rest of the source
COPY . .

# Create a non-root user and hand over ownership of the working directory
RUN groupadd --system appuser \
  && useradd --system --gid appuser --home /app appuser \
  && mkdir -p /app/data \
  && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Default command is production-ready uvicorn.
# docker-compose.yml overrides this with fastapi dev for local development.
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
