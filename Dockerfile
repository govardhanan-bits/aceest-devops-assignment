# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:0

# Install system dependencies for tkinter and GUI
RUN apt-get update && apt-get install -y \
    python3-tk \
    xvfb \
    x11-apps \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN groupadd -r aceest && useradd -r -g aceest aceest
RUN chown -R aceest:aceest /app
USER aceest

# Create directory for database
RUN mkdir -p /app/data

# Expose port (if web interface is added later)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD python -c "import sqlite3; conn = sqlite3.connect('/app/data/aceest_fitness.db'); conn.close()" || exit 1

# Command to run the application
CMD ["python", "Aceestver-3.2.4.py"]
