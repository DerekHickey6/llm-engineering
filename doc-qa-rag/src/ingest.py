import chromadb
from pypdf import PdfReader
import ollama

# Load the pdf
def ingest(pdf_path, collection_name="datamining"):
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


# Test
if __name__ == "__main__":
    text = ingest("C:\\Users\\derek\\Desktop\\llm-engineering\\doc-qa-rag\\data\\Intro-to-Data-Mining.pdf")
    chunked_text = chunk_text(text)
    embeddings = embed_chunks(chunked_text)
    print(len(embeddings))
    print(len(embeddings[0]))