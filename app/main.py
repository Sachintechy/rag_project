from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from pydantic import BaseModel
from typing import List
from app.services.ingestion import ingest_document
from app.services.rag import process_question
from app.database import init_db

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_db()

class QueryRequest(BaseModel):
    question: str
    document_ids: List[int]

class DocumentSelection(BaseModel):
    selected_ids: List[int]

@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    background_tasks.add_task(ingest_document, file)
    return {"status": "Ingestion started"}

@app.post("/documents/select")
async def select_documents(selection: DocumentSelection):
    return {"status": "Selection received", "selected_ids": selection.selected_ids}

@app.post("/qa/query")
async def query_rag(request: QueryRequest):
    answer = await process_question(request.question, request.document_ids)
    return {"answer": answer}
