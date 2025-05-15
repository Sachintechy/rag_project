from fastapi import UploadFile
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from app.models import Document, Embedding
from app.database import SessionLocal
import faiss
import numpy as np

async def ingest_document(file: UploadFile):
    content = await file.read()
    text = content.decode("utf-8")
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(text)
    
    embedder = HuggingFaceEmbeddings()
    vectors = embedder.embed_documents(chunks)

    async with SessionLocal() as session:
        doc = Document(name=file.filename, content=text)
        session.add(doc)
        await session.commit()
        await session.refresh(doc)

        for vec in vectors:
            emb = Embedding(document_id=doc.id, vector=str(vec.tolist()))
            session.add(emb)
        await session.commit()

    index = faiss.IndexFlatL2(len(vectors[0]))
    index.add(np.array(vectors).astype("float32"))
