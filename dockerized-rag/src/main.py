from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from retriever import retriever
from ingest import run_ingest
import ollama
import shutil
import os

api = FastAPI()

class RequestModel(BaseModel):
    question: str = Field(..., description="Question Asked")

class ResponseModel(BaseModel):
    answer: str = Field(..., description="Answer from model")

# Ask question
@api.post("/ask", response_model=ResponseModel)
def ask_question(request: RequestModel):
    try:
        query = request.question
        chunks = retriever(query)
        context = "\n\n".join(chunks)
        prompt = f"""
        Use the following context to answer the question.

        Context:{context}

        Question: {query}
        """

        response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
        return {"answer": response.message.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Upload and ingest a PDF
@api.post("/ingest")
async def ingest_pdf(file: UploadFile = File(...)):
    try:
        save_path = f"/app/data/{file.filename}"
        os.makedirs("/app/data", exist_ok=True)

        with open(save_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        run_ingest(save_path)

        return {"message": f"{file.filename} ingested successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
