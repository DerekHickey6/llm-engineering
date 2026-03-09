from anthropic import Anthropic
from dotenv import load_dotenv
import os
from tools import get_current_time, calculator, web_search, read_file

# Load variables from .env file
load_dotenv()

# Setup conversation history
conversation_history = []

# Initialize client
client = Anthropic()

tools = [
    {
        "name": "get_current_time",
        "description": "Get the current local time",
        "input_schema": {
            "type": "object",
            "properties": {},
        }
    },
    {
    "name": "calculator",
    "description": "Used to evaluate math expression",
    "input_schema": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "math expression to be evaluated"
            }
        },
        "required": ["expression"]
        }
    },
    {
    "name": "read_file",
    "description": "used to read a given file",
    "input_schema": {
        "type": "object",
        "properties": {
            "filepath": {
                "type": "string",
                "description": "filepath to be read"
            }
        },
        "required": ["filepath"]
        }
    },
    {
    "name": "web_search",
    "description": "Searches web browser on duckduckgo for a given query",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "query to be searched for"
            }
        },
        "required": ["query"]
        }
    }

]

# gets response from agent
def agent_response(prompt):

    conversation_history.append({"role": "user", "content": prompt})

    # API call
    while True:
        response = client.messages.create(model="claude-haiku-4-5-20251001",
                                        max_tokens=1024,
                                        messages=conversation_history,
                                        tools=tools,)
        if response.stop_reason == "end_turn":
            # Extract text
            text = response.content[0].text
            conversation_history.append({"role": "assistant", "content": text})

            return text
        elif response.stop_reason == "tool_use":

            # Find the tool_use block in response.content
            tool_use_block = next(block for block in response.content if block.type == "tool_use")

            # Get tool name and inputs
            tool_name = tool_use_block.name
            tool_input = tool_use_block.input

            # Map tool names to functions and execute
            tool_map = {
                "get_current_time": get_current_time,
                "calculator": calculator,
                "read_file": read_file,
                "web_search": web_search
            }

            result = tool_map[tool_name](**tool_input)
            
            conversation_history.append({"role": "assistant", "content": response.content})

            # Append assistant response to history
            conversation_history.append({
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_use_block.id,
                    "content": str(result)
                }]
            })

