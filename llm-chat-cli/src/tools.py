# This file contains tools that can be used by the LLM in the chat CLI.
import requests
import math
from datetime import datetime

def get_current_time():

    return datetime.now().isoformat()

def calculator(expression):
    try:
        result = eval(expression, {"__builtins__": {}}, vars(math))
        return result

    except Exception:
        return "Invalid Expression! Please try again"

def read_file(filepath):
    try:
        with open(filepath, 'r') as f:
            text = f.read()

        return text
    except Exception:
        return "Incorrect filepath format! Please try again"

def web_search(query):
    try:
        # GET request
        response = requests.get("https://api.duckduckgo.com/", params={"q": query, "format": "json", "no_redirect": "1"})

        # Parse JSON
        data = response.json()

        # Try abstract text first
        if data['AbstractText']:
            return data['AbstractText']

        # Fallback
        # Fall back to RelatedTopics
        topics = data["RelatedTopics"][:3]
        return "\n".join([t["Text"] for t in topics if "Text" in t])


    except Exception:
        return "Search Failed! Please try again"