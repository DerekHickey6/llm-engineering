# LLM Evaluation & Observability Framework

An evaluation and logging framework for RAG (Retrieval-Augmented Generation) pipelines. Uses RAGAS to score LLM responses across three metrics and logs every interaction to a structured JSON Lines file for analysis.

## What It Does

1. Runs a set of test questions through a local RAG pipeline (ChromaDB + Ollama)
2. Evaluates each response using RAGAS — scoring faithfulness, answer relevancy, and context recall
3. Logs every interaction (question, context, answer, latency, scores, timestamp) to `log/interactions.jsonl`

## Evaluation Metrics

| Metric | What It Measures |
|---|---|
| **Faithfulness** | Is the answer grounded in the retrieved context? |
| **Answer Relevancy** | Does the answer actually address the question? |
| **Context Recall** | Did the retrieved context contain the information needed? |

Scores range from 0.0 to 1.0. Higher is better.

## Tech Stack

- **RAGAS** — RAG evaluation framework
- **LangChain + langchain-ollama** — LLM and embeddings interface
- **Ollama** — runs `llama3.2` locally for generation and evaluation
- **ChromaDB** — vector store for document retrieval
- **Hugging Face `datasets`** — required by RAGAS internally
- **python-dotenv** — loads LangSmith tracing config from `.env`

## Project Structure

```
llm-eval/
├── src/
│   ├── evaluator.py    # RAGAS scoring logic
│   ├── logger.py       # Structured JSON Lines logging
│   └── main.py         # RAG pipeline + evaluation loop
├── log/
│   └── interactions.jsonl  # Logged evaluation results
├── .env                # LangSmith config (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Pull required Ollama models**
```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

**3. Ingest your documents into ChromaDB**

Place your PDF in the project directory and run the ingest script to populate the vector store before running evaluations.

**4. Configure `.env`**
```
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-key
LANGCHAIN_PROJECT=llm-eval
```

## Usage

```bash
python src/main.py
```

Results are printed to the console and appended to `log/interactions.jsonl`.

## Key Concepts

- **RAGAS** — evaluates RAG pipelines without needing human-labeled data for most metrics
- **`LangchainLLMWrapper` / `LangchainEmbeddingsWrapper`** — adapters that let RAGAS use LangChain-compatible LLMs instead of defaulting to OpenAI
- **`RunConfig(timeout=300)`** — overrides RAGAS's default timeout, necessary when running local LLMs which are slower than cloud APIs
- **JSON Lines (`.jsonl`)** — one JSON object per line, ideal for append-only logging and streaming analysis
- **Golden dataset** — a set of questions with known correct answers used to benchmark system quality over time
