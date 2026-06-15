# RAG Learning Starter

A minimal, educational RAG (Retrieval-Augmented Generation) pipeline from scratch.

## Features

- PDF text extraction
- Chunking with configurable size & overlap
- Embedding generation using `sentence-transformers/all-MiniLM-L6-v2`
- Vector storage & similarity search with PostgreSQL + pgvector
- (Optional) LLM-based answer generation using Ollama (local, free) or OpenAI API

> **Note**: The LLM part is **not tested** due to limited resources (10GB RAM/disk). You may enable it by installing Ollama or adding an OpenAI API key.

## Requirements

- Docker & Docker Compose
- Python 3.10+
- (Optional) Ollama or OpenAI API key

## Setup

### 1. Start PostgreSQL with pgvector

```bash
docker-compose up -d