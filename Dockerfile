# ============================================================================
# Vault Copilot — Multi-stage Dockerfile
# ============================================================================
FROM python:3.11-slim AS base

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System dependencies for EasyOCR and image processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ---------------------------------------------------------------------------
# Stage: Dependencies
# ---------------------------------------------------------------------------
FROM base AS deps

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------------------------------------------------------------------------
# Stage: Application
# ---------------------------------------------------------------------------
FROM deps AS app

# Create non-root user for security
RUN groupadd -r vault && useradd -r -g vault -d /app vault

# Copy application code
COPY src/ src/
COPY eval/ eval/
COPY .env.example .env.example
COPY docker-entrypoint.sh /app/docker-entrypoint.sh

# Create data directories
RUN mkdir -p raw_receipts chroma_db logs data \
    && chown -R vault:vault /app \
    && chmod +x /app/docker-entrypoint.sh

USER vault

# Default: run both services together (Docker Compose overrides this command)
EXPOSE 7860 8001
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["combined"]
