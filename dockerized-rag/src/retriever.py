import ollama
import chromadb

def retriever(query, n_results=5, collection='datamining'):
    client = chromadb.PersistentClient('/chroma_db')

    collection = client.get_collection(collection)

    embedded_query = ollama.embeddings(model="nomic-embed-text", prompt=query)["embedding"]
    results_dict = collection.query(query_embeddings=[embedded_query],
                     n_results=n_results)

    chunks = results_dict['documents'][0]

    return chunks

if __name__ == "__main__":
    query = "what is clustering"
    print(retriever(query))