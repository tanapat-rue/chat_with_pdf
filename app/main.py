import os
from fastapi import FastAPI, HTTPException
from langchain_openai import OpenAI
from pydantic import BaseModel

from rag import Rag
from assistant import Assistant
from evaluation import Evaluation
from typing import Any

# Initialize FastAPI app
app = FastAPI()


rag = Rag()
assistant = Assistant()
evaluation = Evaluation()


@app.post("/process_papers")
def process_papers():
    """Read PDFs from 'papers' folder, embed text, and store in PostgreSQL with chunking."""
    print("Processing papers with chunking...")
    for filename in os.listdir("papers"):
        print(f"Processing file: {filename}")
        if filename.endswith(".pdf"):
            file_path = os.path.join("papers", filename)
            text = rag.extract_text_from_pdf(file_path)
            print(f"Extracted text length: {len(text)} characters")
            chunks = rag.chunk_text(text)
            print(f"Total chunks created: {len(chunks)}")
            for idx, chunk in enumerate(chunks):
                print(f"Embedding chunk {idx+1}/{len(chunks)}")
                vector = rag.embed_text(chunk)
                rag.store_embedding(vector, chunk, filename)
    return {"status": "Processed all papers in the 'papers' folder with chunking."}



class ChatRequest(BaseModel):
    prompt: str
    email: str = "test@mail.com"
    refresh: bool = False

@app.post("/testchat")
def chattest(req: ChatRequest):
    return assistant.get_response_test(req.prompt)



@app.post("/chat")
def chat(req: ChatRequest):
    response = assistant.get_response(prompt=req.prompt, session_id=req.email, refresh=req.refresh)
    return {"response": response}


class Response(BaseModel):
    df: list[dict[str, Any]]
    
@app.post("/evaluation")
def evaluate():
    df = evaluation.evaluate_model(assistant, rag)
    return Response(
        df=df.to_dict(orient="records"),
    )



@app.get("/status")
def status():
    return {"message": "Welcome to the PDF chat application with PostgreSQL vector support!"}
