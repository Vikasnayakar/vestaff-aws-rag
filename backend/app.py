from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import time

from backend.rag_engine import RAGEngine


app = FastAPI(
    title="RAG Analytics Server"
)


# IMPORTANT: only one instance
rag = RAGEngine()



class QueryRequest(BaseModel):
    query: str



@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):

    file_path = "aws_customer_agreement.pdf"


    with open(file_path, "wb") as f:
        f.write(await file.read())


    chunks = rag.ingest_document(file_path)


    return {
        "status":"success",
        "chunks_processed":chunks
    }



@app.post("/ask")
async def ask_question(payload: QueryRequest):

    start = time.time()


    result = rag.query(
        payload.query
    )


    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "latency_seconds": round(
            time.time()-start,
            3
        )
    }