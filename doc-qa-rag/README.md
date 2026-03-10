# Document Q&A with RAG + Ollama

A fully local Retrieval-Augmented Generation (RAG) pipeline that answers questions grounded in a PDF document. No cloud APIs or internet connection required at inference time.

## Overview

This project ingests a PDF textbook, chunks and embeds the text into a local ChromaDB vector database, and uses semantic search to retrieve relevant context for any user query. The retrieved chunks are passed to a local LLM (`llama3.2` via Ollama) to generate accurate, grounded answers.

## Features

- Fully local — embeddings, vector storage, and generation all run on your machine
- Semantic search over a PDF using `nomic-embed-text` embeddings
- Grounded answers from `llama3.2` — responses are tied to actual document content
- Modular three-file pipeline: ingest → retrieve → generate

## RAG Pipeline

```
PDF → chunk text → embed chunks → store in ChromaDB
                                          ↓
Query → embed query → semantic search → top-k chunks → prompt → llama3.2 → answer
```

| Step | File | Description |
|---|---|---|
| Ingest | `ingest.py` | Loads PDF, chunks text, embeds with `nomic-embed-text`, stores in ChromaDB |
| Retrieve | `retriever.py` | Embeds query, searches ChromaDB, returns top-k relevant chunks |
| Generate | `rag.py` | Builds prompt from chunks + query, sends to `llama3.2`, returns answer |

## Models

| Model | Role | Runtime |
|---|---|---|
| `nomic-embed-text` | Text embeddings | Ollama (local) |
| `llama3.2` | Answer generation | Ollama (local) |

## Project Structure

```
doc-qa-rag/
├── src/
│   ├── ingest.py        # Load → chunk → embed → store
│   ├── retriever.py     # Query ChromaDB for relevant chunks
│   └── rag.py           # Orchestrate full pipeline
├── data/                # Place your PDF here (gitignored)
├── chroma_db/           # Vector database (gitignored, built by ingest.py)
├── .gitignore
├── requirements.txt
└── README.md
```

## How to Run

### 1. Install Ollama
Download from [ollama.com](https://ollama.com) and pull the required models:
```bash
ollama pull nomic-embed-text
ollama pull llama3.2
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your PDF
Place your PDF in the `data/` folder and update the path in `ingest.py`.

### 4. Ingest the document
Run once to build the vector database (takes a few minutes):
```bash
python src/ingest.py
```

### 5. Ask questions
```bash
python src/rag.py
```
