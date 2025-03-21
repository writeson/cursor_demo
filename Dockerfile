FROM python:3.12.7-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Create app user with proper home directory
RUN mkdir -p /home/app_user && \
    groupadd -r app_user && \
    useradd -r -g app_user -d /home/app_user app_user && \
    chown -R app_user:app_user /home/app_user

# Create database directory and ensure permissions
RUN mkdir -p /app/project/db && \
    chown -R app_user:app_user /app

# Switch to non-root user
USER app_user

# Install dependencies using pip with user flag
RUN pip install --user --no-cache-dir -e .

# Add user's local bin to PATH
ENV PATH="/home/app_user/.local/bin:$PATH"

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "project.src.main:app", "--host", "0.0.0.0", "--port", "8000"]