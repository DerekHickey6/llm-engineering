import time

from evaluator import evaluate_rag
from logger import log_interaction
from chromadb import PersistentClient
import ollama
from dotenv import load_dotenv

load_dotenv()

test_cases = [
    {
        "question": "What is data mining?",
        "ground_truth": "Data mining is the process of discovering patterns, correlations, and insights from large datasets using statistical and computational techniques."
    },
    {
        "question": "What are common data mining techniques?",
        "ground_truth": "Common data mining techniques include classification, clustering, regression, association rule mining, and anomaly detection."
    },
    {
        "question": "What is the difference between supervised and unsupervised learning in data mining?",
        "ground_truth": "Supervised learning uses labeled data to train models for prediction, while unsupervised learning finds hidden patterns in unlabeled data without predefined outputs."
    }
]

def retrieve(question, collection_name='datamining'):
    client = PersistentClient("/chroma_db")
    collection = client.get_collection(collection_name)

    embedded_query = ollama.embeddings(model="nomic-embed-text", prompt=question)["embedding"]
    results_dict = collection.query([embedded_query])

    chunks = results_dict["documents"][0]

    return chunks

def generate(question, context):

    prompt = f"""
    Use the following context to answer the question:

    Context:
    {context}

    Question:
    {question}
    """
    response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
    return response.message.content

if __name__ == "__main__":

    for case in test_cases:
        question = case['question']
        ground_truth = case['ground_truth']

        start_time = time.time()
        chunks = retrieve(question)
        context = "\n\n".join(chunks)
        response = generate(question, chunks)
        stop_time = time.time()

        latency = stop_time - start_time

        scores = evaluate_rag(question, context, response, ground_truth)
        scores_dict = scores.to_pandas().to_dict(orient="records")[0]
        log_interaction(question, context, response, latency, scores_dict)
        print(scores)
