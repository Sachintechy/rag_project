# Document RAG Q&A Application (MySQL Version)

## 🚀 Overview
A FastAPI backend that allows:
- Uploading documents
- Generating embeddings and storing in MySQL
- Answering user questions using RAG with FAISS + LLM

## 🧰 Tech Stack
- FastAPI
- MySQL + SQLAlchemy
- FAISS for similarity search
- LangChain + OpenAI or HuggingFace
- Docker + GitHub Actions CI/CD

## 📦 Running Locally
### Prerequisites
- Docker and Docker Compose

### Start App
```bash
docker-compose up --build
```

## 🧪 Endpoints
- `POST /documents/upload` - Upload and ingest document
- `POST /documents/select` - Select documents by ID
- `POST /qa/query` - Ask question using selected documents

## 🔐 Environment
Update `DATABASE_URL` in `.env` or `docker-compose.yml` as needed.
