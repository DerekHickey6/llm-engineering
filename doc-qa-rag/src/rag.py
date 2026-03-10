import ollama
import sys
import os

sys.path.append(os.getcwd())
from src.retriever import retrieve

## Take Query -> Retrieve Chunks -> Build a prompt -> send to llama3.2

def ask(query):
    chunks = retrieve(query=query)

    prompt = f"""
    Use the following context to answer the question.

    Context:{"\n\n".join(chunks)}

    Question: {query}
    """

    response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])

    response = response['message']['content']

    return response

if __name__ == "__main__":
    query = "how to i find association rules for a frequent 4-itemset?"
    print(ask(query))
