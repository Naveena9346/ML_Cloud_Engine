# Root Dockerfile for MLCloudEngine Platform
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy application source code
COPY . /app

# Expose FastAPI backend port
EXPOSE 8000

# Set entry point
CMD ["python", "run_server.py"]
