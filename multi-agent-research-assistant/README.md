# Multi-Agent Research Assistant

A multi-agent research pipeline built with LangGraph. Given a topic, three specialized agents collaborate to break it down, search the web, and synthesize a written summary.

## How It Works

The pipeline runs as a directed graph with three nodes executing in sequence:

1. **Planner Node** — takes the topic, uses an LLM to generate 3 focused sub-questions to research
2. **Searcher Node** — runs each sub-question through DuckDuckGo search and collects the results
3. **Writer Node** — synthesizes all search results into a coherent written summary using an LLM

## Tech Stack

- **LangGraph** — builds and runs the multi-agent state graph
- **LangChain** — prompt templating and LCEL chain composition
- **langchain-ollama** — local LLM integration via Ollama
- **langchain-community** — DuckDuckGo search tool
- **Ollama** — runs `llama3.2` locally

## Project Structure

```
multi-agent-research-assistant/
├── src/
│   ├── agents.py      # Planner, searcher, and writer node functions + ResearchState
│   ├── graph.py       # StateGraph definition, edges, and compilation
│   └── main.py        # Entry point — invokes the graph with a topic
├── .env               # Environment variables (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Pull the model**
```bash
ollama pull llama3.2
```

## Usage

Edit the topic in `main.py`:

```python
result = app.invoke({"topic": "your topic here"})
```

Then run:

```bash
python src/main.py
```

## Key Concepts

- **StateGraph** — LangGraph's core abstraction; nodes read from and write to a shared state dict
- **ResearchState** — a `TypedDict` schema defining the keys passed between nodes (`topic`, `sub_questions`, `results`, `summary`)
- **Nodes** — plain Python functions that take state and return a dict of updated keys
- **Edges** — define execution order; `add_edge("a", "b")` means b runs after a
- **LCEL** — pipe operator chains `prompt | llm | parser` into a single runnable
