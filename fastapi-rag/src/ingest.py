import chromadb
from pypdf import PdfReader
import ollama

datamining_path = "C:\\Users\\derek\\Desktop\\llm-engineering\\doc-qa-rag\\data\\Intro-to-Data-Mining.pdf"

# Load the pdf
def ingest(pdf_path):
    pdf = PdfReader(pdf_path)
    page_text = []

    # Extracts page text
    for page in pdf.pages:
        text = page.extract_text()
        if text is not None:
            page_text.append(text)

    page_text = "".join(page_text)
    return page_text

# Chunk text with overlap
def chunk_text(text, chunk_size=500, overlap=50):
    chunked_text = []

    for i in range(0, len(text), chunk_size - overlap):
        chunked_text.append(text[i:i+chunk_size])

    return chunked_text

# Embed the chunks
def embed_chunks(chunks):
    embeddings = []

    for chunk in chunks:
        embeddings.append(ollama.embeddings(model="nomic-embed-text", prompt=chunk)["embedding"])

    return embeddings

# Store in persistant chromaDB locally
def store_in_chromadb(chunks, embeddings, collection_name="datamining"):
    persistant_client = chromadb.PersistentClient(path="./chroma_db")
    collection = persistant_client.get_or_create_collection(name=collection_name)

    collection.add(documents=chunks,
                   embeddings=embeddings,
                   ids=[f"chunk_{i}" for i in range(len(chunks))])

# Convenience method for running all ingest functions
def run_ingest(pdf_path):
    chunks = chunk_text(ingest(pdf_path))
    store_in_chromadb(chunks=chunks, embeddings=embed_chunks(chunks))

# Test
if __name__ == "__main__":
    run_ingest(datamining_path)

    # text = ingest("C:\\Users\\derek\\Desktop\\llm-engineering\\doc-qa-rag\\data\\Intro-to-Data-Mining.pdf")
    # chunked_text = chunk_text(text)
    # embeddings = embed_chunks(chunked_text)
    # store_in_chromadb(chunked_text, embeddings)
    # print(len(embeddings))
    # print(len(embeddings[0]))