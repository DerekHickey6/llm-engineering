# Dockerized RAG API

## Overview
A fully containerized Retrieval-Augmented Generation (RAG) API built with FastAPI, ChromaDB, and Ollama. Upload any PDF and query it with natural language — all running inside Docker with no local Python or Ollama setup required.

## Features
- `POST /ingest` — upload a PDF, embed it, and store it in ChromaDB
- `POST /ask` — ask a natural language question grounded in the ingested PDF
- Fully containerized with Docker and Docker Compose
- ChromaDB and Ollama model data persist across container restarts via volumes

## Tech Stack
- **FastAPI** — REST API framework
- **ChromaDB** — vector store for document embeddings
- **Ollama** — local LLM inference (`llama3.2`) and embeddings (`nomic-embed-text`)
- **pypdf** — PDF text extraction
- **Docker + Docker Compose** — containerization and orchestration

## Architecture
```
Client
  │
  ▼
FastAPI (app container)
  ├── POST /ingest → extract → chunk → embed → store in ChromaDB volume
  └── POST /ask   → embed query → retrieve chunks → prompt Ollama → return answer
                                                          │
                                                    Ollama container
```

## How to Run

### 1. Clone and navigate
```bash
git clone https://github.com/DerekHickey6/llm-engineering.git
cd llm-engineering/dockerized-rag
```

### 2. Start the containers
```bash
docker-compose up --build -d
```

### 3. Pull required models into the Ollama container
```bash
docker exec dockerized-rag-ollama-1 ollama pull llama3.2
docker exec dockerized-rag-ollama-1 ollama pull nomic-embed-text
```

### 4. Ingest a PDF
Use the `/docs` UI at `http://localhost:8000/docs` or curl:
```bash
curl -X POST http://localhost:8000/ingest \
  -F "file=@your_document.pdf"
```

### 5. Ask a question
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Your question here"}'
```

## Project Structure
```
dockerized-rag/
├── src/
│   ├── main.py          # FastAPI app — /ask and /ingest endpoints
│   ├── ingest.py        # PDF extraction, chunking, embedding, ChromaDB storage
│   └── retriever.py     # Query embedding and ChromaDB retrieval
├── data/                # Drop PDFs here (gitignored)
├── Dockerfile           # App container definition
├── docker-compose.yml   # Multi-container orchestration (app + ollama)
├── requirements.txt
└── .gitignore
```
