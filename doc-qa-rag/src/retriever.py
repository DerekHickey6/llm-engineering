import chromadb
import ollama

def retrieve(query, n_results=5, collection_name="datamining"):
    # Connect to ChromaDB to get collection
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(collection_name)

    # Query colletions
    embeded_query = ollama.embeddings(prompt=query, model="nomic-embed-text")["embedding"]
    results_dict = collection.query(query_embeddings=[embeded_query],
                                    n_results=n_results)

    chunks = results_dict["documents"][0]

    return chunks

# Test
if __name__ == "__main__":
    query = "What is hierarchical clustering?"
    output = retrieve(query)
    print(output)
