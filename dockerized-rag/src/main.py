from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from retriever import retriever
import ollama

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

# Upload pdf
from fastapi import UploadFile, File

@api.post("/ingest")
async def ingest_pdf(file: UploadFile = File(...)):
    pass
