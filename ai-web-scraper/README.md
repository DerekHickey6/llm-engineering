# AI Web Scraper

A LangChain-powered web scraper that fetches a webpage, extracts its text content, and answers natural language questions about it using a local LLM via Ollama.

## How It Works

1. Sends an HTTP GET request to the target URL
2. Parses the HTML response with BeautifulSoup
3. Cleans and truncates the extracted text
4. Passes the text + user question through a LangChain LCEL pipeline
5. Returns a grounded answer from the local LLM

## Tech Stack

- **LangChain** — prompt templating and LCEL pipeline (`|` operator)
- **Ollama** — local LLM inference (`llama3.2`)
- **BeautifulSoup** — HTML parsing and text extraction
- **Requests** — HTTP client

## Setup

**Prerequisites:** [Ollama](https://ollama.com) installed and running with `llama3.2` pulled.

```bash
ollama pull llama3.2
```

**Install dependencies:**

```bash
pip install -r requirements.txt
```

## Usage

```python
from scraper import scrape_web

response = scrape_web(
    url="https://example.com/article",
    query="What is this article about?",
    truncate_size=5000  # optional, default is 5000 characters
)
```

Or run directly:

```bash
python src/scraper.py
```

## Project Structure

```
ai-web-scraper/
├── src/
│   └── scraper.py        # Core scraping and LLM pipeline logic
├── requirements.txt
└── README.md
```

## Notes

- `truncate_size` controls how many characters of page content are passed to the model. Default is 5000 (~1250 tokens), which is enough for most articles while leaving room for the model's response.
- Temperature is set to `0.1` to keep answers grounded in the page content rather than hallucinated.
