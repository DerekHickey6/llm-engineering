# MCP Server

A custom MCP (Model Context Protocol) server that exposes three tools to any compatible AI client (Claude Desktop, Cursor, etc.). Built with FastMCP and LangChain.

## What It Does

Exposes three tools that Claude Desktop can discover and call automatically:

| Tool | Description |
|---|---|
| `search_web(query)` | Searches the web using DuckDuckGo |
| `get_weather(city)` | Returns live weather for any city via Open-Meteo API |
| `summarize(text)` | Summarizes text using a local LLM via Ollama |

## Tech Stack

- **FastMCP** — high-level MCP server framework (Anthropic's Model Context Protocol)
- **LangChain** — LCEL chain for the summarize tool
- **langchain-ollama** — local LLM integration (`llama3.2`)
- **langchain-community** — `DuckDuckGoSearchRun` tool
- **Open-Meteo API** — free weather + geocoding API, no key required
- **requests** — HTTP calls to Open-Meteo

## Project Structure

```
mcp-server/
├── src/
│   └── server.py      # MCP server with all three tool definitions
├── requirements.txt
├── .gitignore
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

**3. Register with Claude Desktop**

Add the following to your `claude_desktop_config.json` (located at `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["C:\\path\\to\\mcp-server\\src\\server.py"]
    }
  }
}
```

Restart Claude Desktop — the server will start automatically and your tools will be available.

## Usage

Once connected, ask Claude Desktop directly:

- `"Use the get_weather tool to get the weather in Vancouver."`
- `"Use search_web to find recent news about LangGraph."`
- `"Use summarize to summarize this text: ..."`

## Key Concepts

- **MCP (Model Context Protocol)** — open standard by Anthropic for exposing tools to AI clients in a standardized way. Think USB-C for AI tools.
- **FastMCP** — decorator-based framework for defining MCP tools. The `@mcp.tool()` decorator registers a function and its docstring as a callable tool.
- **Claude Desktop as MCP client** — launches the server process automatically using the config, discovers tools, and calls them based on context.
- **LCEL chain** — `prompt | llm | parser` pattern used in the `summarize` tool.
