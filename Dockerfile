FROM python:3.12.7-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Create app user
RUN groupadd -r app_user && useradd -r -g app_user app_user

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml ./
RUN pip install --upgrade pip && \
    pip install . && \
    pip install uv

# Create app directories
RUN mkdir -p /app/project/db && \
    chown -R app_user:app_user /app

# Copy project files
COPY . .

# Make db directory writable
RUN chown -R app_user:app_user /app/project/db

# Set user
USER app_user

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "project/main.py"]