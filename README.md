# AWS Customer Agreement RAG Assistant

A Retrieval Augmented Generation (RAG) application that allows users to upload the AWS Customer Agreement PDF and ask questions based on the document content.

The system extracts text from the PDF, creates embeddings, stores them in a vector database, retrieves relevant document chunks, and generates answers using a local LLM.

## Features

- PDF document ingestion
- Automatic text extraction and chunking
- Semantic search using vector embeddings
- FAISS vector database for document retrieval
- Local LLM inference using Ollama
- Question answering based only on uploaded document content
- Source chunk display for transparency
- Query analytics and latency tracking
- FastAPI backend API
- Streamlit user interface

## Tech Stack

Backend:
- FastAPI
- Python
- LangChain
- FAISS
- Sentence Transformers
- Ollama

Frontend:
- Streamlit

Database:
- SQLite (for analytics storage)

## Project Structure
aws-rag-assignment/
│
├── backend/
│ ├── app.py
│ ├── rag_engine.py
│ ├── config.py
│ └── database.py
│
├── frontend/
│ └── dashboard.py
│
├── documents/
│ └── aws_customer_agreement.pdf
│
├── requirements.txt
└── README.md

## Installation

step 1: Clone the repository: cd aws-rag-assignment
step 2: Move into project directory: cd aws-rag-assignment
step 3: Create virtual environment: python -m venv venv
step 4:Activate environment: Windows: venv\Scripts\activate
step 5: Install dependencies: pip install -r requirements.txt

## Setup Ollama

step 1: Install Ollama and download the model:
step 2: Verify model: ollama list

## Running Backend

Start FastAPI server: uvicorn backend.app:app --reload
Backend will run on: http://127.0.0.1:8000


API documentation: http://127.0.0.1:8000/docs

## Document Ingestion

Upload AWS Customer Agreement PDF using the `/ingest` endpoint.

Example response:

```json
{
  "status": "success",
  "chunks_processed": 131
}

Running Frontend :

step 1: Start Streamlit: streamlit run frontend/dashboard.py
step 2: Frontend runs on: http://localhost:8501

API Endpoints :

step 1: POST /ingest
 Uploads and processes a PDF document.
-Input:
 multipart/form-data
 file: pdf document
step 2: POST /ask
Ask questions from the uploaded document.

Request:
{
  "query": "What is the limitation of liability?"
}
Response:
{
  "answer": "Generated answer from document context",
  "sources": [
    "Relevant document chunks"
  ],
  "latency_seconds": 2.5
}
step 3: GET /analytics
Returns system usage information.

Includes:
Average response latency
Number of unanswered queries
Frequently asked questions

Design Decisions

Example:

Chunking Strategy

I used RecursiveCharacterTextSplitter with a chunk size of 400 characters and overlap of 50 characters. This helps maintain enough context between chunks while avoiding unnecessary large inputs to the LLM.

Embedding Model

Sentence Transformer (all-MiniLM-L6-v2) was selected because it provides lightweight semantic embeddings suitable for document retrieval.

Vector Database

FAISS was used because it provides fast similarity search and does not require external hosting.

Retrieval

The system retrieves the most relevant document chunk using similarity search before generating the final response.

LLM Choice

Ollama with Llama 3.2 was used as a local model to avoid paid API dependency.

Example Questions :

1. What is the limitation of liability?
2. What are AWS payment obligations?
3. How can the agreement be terminated?
4. What rights does AWS have regarding service usage?
5. What happens if services become unavailable?
6. What are the customer's responsibilities?

RAG Pipeline :

step 1: User uploads AWS agreement PDF
step 2: PDF text is extracted
step 3: Text is split into smaller chunks
step 4: Embeddings are generated using Sentence Transformers
step 5: Chunks are stored in FAISS vector database
step 6: User question is converted into an embedding
step 7: Relevant chunks are retrieved
step 8: Retrieved context is passed to Ollama LLM
step 9: Final answer is generated using document context

Limitations :

1. Answers depend only on the uploaded document
2. Large documents may increase processing time
3. Local LLM performance depends on available hardware

Future Improvements :

1. Add authentication
2. Store multiple documents
3. Add document management
4. Improve retrieval ranking
5. Deploy using Docker and cloud services
