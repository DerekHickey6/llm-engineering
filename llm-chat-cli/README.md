# LLM Chat CLI + Tool Use Agent

A command-line AI agent powered by the Anthropic Claude API. Supports multi-turn conversation with persistent history and real-world tool use — the model reasons and responds while tools extend its capabilities beyond static training data.

## Overview

Demonstrates the core pattern behind modern AI agents: a pretrained language model paired with tools that allow it to act in the world. The agent loop handles both standard conversational responses and tool-calling, giving Claude the ability to look up live information, perform calculations, and read files — all from the terminal.

## Features

- Multi-turn conversation with full history maintained across turns
- Tool use agent loop — detects `tool_use` stop reason, executes tools, returns results to Claude
- `get_current_time` — returns current local date and time
- `calculator` — safely evaluates math expressions using a restricted `eval` with `math` module scope
- `web_search` — queries DuckDuckGo Instant Answer API for live web results (no API key required)
- `read_file` — reads any file from a given path and returns its contents
- Clean CLI entry point with graceful exit

## Agent Loop

The agent is stateless at the API level — Claude does not retain memory between calls. Conversation history is maintained client-side and sent in full with every request.

When Claude decides to use a tool:
1. `stop_reason == "tool_use"` is returned instead of `"end_turn"`
2. The tool use block is extracted from `response.content`
3. The matching Python function is called with the provided arguments
4. The assistant response and tool result are appended to history
5. A new API call is made — Claude sees the result and generates a final response

This loop repeats until `stop_reason == "end_turn"`.

## Project Structure

```
llm-chat-cli/
├── src/
│   ├── agent.py        # Anthropic client, tool schemas, agent loop
│   ├── tools.py        # Tool function implementations
│   └── cli.py          # Entry point, input/output loop
├── .env                # API key (gitignored)
├── requirements.txt
└── README.md
```

## How to Run

1. Install dependencies:
```bash
pip install anthropic python-dotenv requests
```

2. Add your Anthropic API key to `.env`:
```
ANTHROPIC_API_KEY=your-key-here
```

3. Run the CLI:
```bash
python src/cli.py
```

4. Example prompts to try:
- `"What time is it?"`
- `"What is the square root of 1764?"`
- `"Search for the Python programming language"`
- `"Read the file src/tools.py"`
