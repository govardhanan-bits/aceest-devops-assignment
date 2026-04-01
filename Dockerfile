# Use Python 3.10 slim image as base for smaller image size
FROM python:3.10-slim

# Set metadata labels
LABEL maintainer="ACEest DevOps Team"
LABEL description="ACEest Fitness Application - DevOps Implementation"
LABEL version="1.0.0"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_HOST=0.0.0.0 \
    FLASK_PORT=5000

# Set work directory
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
# Use --no-cache-dir to reduce image size
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir flask pytest && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Create directory for database with proper permissions
RUN mkdir -p /app/data && chmod 755 /app/data

# Create non-root user for security best practices
RUN groupadd -r aceest && \
    useradd -r -g aceest -d /app -s /bin/bash aceest && \
    chown -R aceest:aceest /app

# Switch to non-root user
USER aceest

# Expose application port
EXPOSE 5000

# Health check to ensure container is running properly
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')" || exit 1

# Run the application
CMD ["python", "app.py"]
