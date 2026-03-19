import chromadb
from pypdf import PdfReader
import ollama

# Ingest -> Chunk -> Embed -> Store

def ingest(pdfpath):
    reader = PdfReader(pdfpath)
    extracted_text = []

    for page in reader.pages:
        text = page.extract_text()
        if text is not None:
            extracted_text.append(text)

    extracted_text = "".join(extracted_text)
    return extracted_text


def chunk_text(text, len_chunks=500, offset=50):
    chunks = []

    for i in range(0, len(text)//len_chunks, offset):
        chunks.append(text[i:i+len_chunks])

    return chunks


def embed_chunks(chunks):
    embeddings = []
    for chunk in chunks:
        embeddings.append(ollama.embeddings(model='nomic-embed-text', prompt=chunk)['embedding'])

    return embeddings


def store_db(chunks, embeddings, collection='datamining'):
    client = chromadb.PersistentClient('/chroma_db')
    collection = client.get_or_create_collection(name=collection)

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"Chunk_{i}" for i in range(len(chunks))]
    )

def run_ingest(pdfpath):
    chunks = chunk_text(ingest(pdfpath))

    return store_db(chunks, embed_chunks(chunks))

if __name__ == "__main__":
    pdfpath = "C:\\Users\\derek\\Desktop\\llm-engineering\\llm-eval\\data\\Intro_to_Data_Mining.pdf"

    run_ingest(pdfpath=pdfpath)