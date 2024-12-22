FROM python:3.9-slim-bookworm

# Add tini for proper init and signal handling in container
RUN apt-get update && \
    apt-get install -y \
    tini \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt boto3

# Copy application code
COPY producer.py .

# Set environment variables for Python logging
ENV PYTHONUNBUFFERED=1

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD ps aux | grep python || exit 1

# Use tini as entrypoint for proper signal handling
ENTRYPOINT ["/usr/bin/tini", "--"]

# Command to run the producer
CMD ["python", "producer.py"]