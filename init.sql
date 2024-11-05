-- init.sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS papers_vectors (
    id SERIAL PRIMARY KEY,
    vector VECTOR(1536) NOT NULL,
    text TEXT NOT NULL,
    paper_name TEXT NOT NULL
);
