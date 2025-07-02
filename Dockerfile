# Use Python 3.9 slim image for smaller size
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies for PIL and other packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .
COPY static/ ./static/

# Create a non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app && \
    mkdir -p /home/appuser/.cache/huggingface && \
    chown -R appuser:appuser /home/appuser/.cache
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/').raise_for_status()" || exit 1

# Run the application
CMD ["python", "main.py"]