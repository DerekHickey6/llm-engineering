from anthropic import Anthropic
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Setup conversation history
conversation_history = []

# Initialize client
client = Anthropic()

# gets response from agent
def agent_response(prompt):

    conversation_history.append({"role": "user", "content": prompt})

    # API call
    response = client.messages.create(model="claude-haiku-4-5-20251001",
                                      max_tokens=1024,
                                      messages=conversation_history)

    # Extract text
    text = response.content[0].text
    conversation_history.append({"role": "assistant", "content": text})

    return text
