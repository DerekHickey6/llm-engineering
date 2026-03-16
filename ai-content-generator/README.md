# AI Content Idea Generator

Generates grounded social media content using real trending headlines from Hugging Face datasets and a local LLM via Ollama and LangChain.

## What It Does

1. Takes a **topic** and optional **content type** as input
2. Fetches relevant headlines from the [heegyu/news-category-dataset](https://huggingface.co/datasets/heegyu/news-category-dataset) on Hugging Face (209k news articles)
3. Injects those headlines as context into a prompt
4. Generates a formatted social media post using `llama3.2` via Ollama
5. Returns the output as a plain string

## Tech Stack

- **LangChain** — prompt templating and LCEL chain composition
- **langchain-ollama** — local LLM integration
- **Ollama** — runs `llama3.2` locally
- **Hugging Face `datasets`** — pulls real-world news headline data
- **python-dotenv** — loads `HF_TOKEN` from `.env`

## Project Structure

```
ai-content-generator/
├── src/
│   └── generator.py       # Core logic: dataset fetch + LLM chain
├── .env                   # HF_TOKEN (not committed)
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

**3. Add your Hugging Face token to `.env`**
```
HF_TOKEN=your-hf-token-here
```
Get a token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) (Read access is sufficient).

## Usage

```bash
python src/generator.py
```

To change the topic or content type, edit the `__main__` block in `generator.py`:

```python
response = generate_ideas("climate change", content_type="Twitter thread")
print(response)
```

## Key Concepts

- **LCEL (LangChain Expression Language)** — pipes components together: `prompt | llm | parser`
- **ChatPromptTemplate** — defines the prompt with named `{variables}` filled at runtime
- **StrOutputParser** — extracts plain string from the `AIMessage` returned by the LLM
- **Hugging Face `datasets`** — `load_dataset()` returns a `DatasetDict`; access data via `dataset["train"]`
