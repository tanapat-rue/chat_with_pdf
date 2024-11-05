# Use Python as the base image
FROM python:3.11.10-slim-bullseye

# Arguments
ARG BUILD_VERSION=dev-xxx

# Install dependencies, PostgreSQL, and pgvector support
RUN apt-get update -y && \
    apt-get install -y gcc libgeos-dev \
                       postgresql postgresql-contrib postgresql-server-dev-all && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install uv==0.1.24
RUN uv pip install --system --no-cache-dir -r requirements.txt


# Switch to the /app directory for the main application
WORKDIR /app

# Set environment variables
ENV BUILD_VERSION=${BUILD_VERSION}
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app:/app/app:$PYTHONPATH

# Expose PostgreSQL and application ports
EXPOSE 5432 8000

# Start PostgreSQL when the container runs
CMD service postgresql start && tail -f /dev/null
