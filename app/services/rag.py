from app.database import SessionLocal
from app.models import Embedding
from langchain.llms import OpenAI
import numpy as np
import faiss
import ast

async def process_question(question: str, document_ids: list):
    async with SessionLocal() as session:
        result = await session.execute(
            f"SELECT vector FROM embeddings WHERE document_id IN ({','.join(map(str, document_ids))})"
        )
        vectors = [ast.literal_eval(row[0]) for row in result.fetchall()]

    index = faiss.IndexFlatL2(len(vectors[0]))
    index.add(np.array(vectors).astype("float32"))

    embedder = OpenAI()
    query_vector = embedder.embed_query(question)
    D, I = index.search(np.array([query_vector]).astype("float32"), k=3)

    top_chunks = [vectors[i] for i in I[0]]
    context = " ".join(map(str, top_chunks))
    return embedder.generate(prompt=f"Answer the question based on context: {context}\nQ: {question}")
