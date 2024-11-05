#!/bin/bash
set -e

# Start PostgreSQL service
service postgresql start

# Wait for PostgreSQL to start
sleep 5

# Set up database variables
DB_NAME="chat_db"
DB_USER="postgres"
DB_PASSWORD="postgres"

# Create vector extension and table if they don't exist
psql -U $DB_USER -d $DB_NAME -c "CREATE EXTENSION IF NOT EXISTS vector;"

psql -U $DB_USER -d $DB_NAME -c "
CREATE TABLE IF NOT EXISTS papers_vectors (
    id SERIAL PRIMARY KEY,
    vector VECTOR(1536) NOT NULL,
    text TEXT NOT NULL,
    paper_name TEXT NOT NULL
);"

# Optionally, you can run any other initialization scripts or start your application here

# Start your application (uncomment and modify the following line as needed)
uvicorn main:app --host 0.0.0.0 --port 8000

# Keep the container running
tail -f /dev/null
