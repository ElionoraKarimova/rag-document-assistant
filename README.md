# RAG Document Assistant

An AI-powered document assistant built with **RAG (Retrieval-Augmented Generation)** and an **AI agent**. Ask questions about your documents and get accurate, context-based answers from a local LLM.

## What it does

Upload documents, and the assistant answers questions based on their content — not from general knowledge. It uses semantic search to find relevant information and a local LLM to generate grounded answers, reducing hallucinations.

It includes two modes:
- **RAG mode** — direct retrieval and answer generation from documents
- **Agent mode** — an AI agent that decides which tools to use to answer

## Tech Stack

- **Python** + **FastAPI** — backend and REST API
- **LangChain** — RAG pipeline and agent orchestration
- **Ollama** (llama3.2) — local LLM for answer generation
- **nomic-embed-text** — embeddings model
- **Chroma** — vector database (semantic search)
- **PostgreSQL** + **SQLAlchemy** — relational database (query history)
- **Docker** and **Docker Compose** — containerized services

## Features

- Document indexing (TXT, PDF) into a vector database
- Semantic search over document content
- RAG-based question answering grounded in documents
- AI agent with tools (ReAct pattern)
- Query history stored in PostgreSQL
- Fully containerized with Docker

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Health check |
| `GET /ask?question=...` | Ask the LLM directly (no RAG) |
| `GET /index?filename=...` | Index a document from the `documents/` folder |
| `GET /rag?question=...` | Ask a question answered from documents (RAG) |
| `GET /agent?question=...` | Ask the AI agent (chooses tools automatically) |
| `GET /history` | View query history |

## How to run

### Prerequisites
- [Docker](https://www.docker.com/) and Docker Compose
- [Ollama](https://ollama.com/) installed locally

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ElionoraKarimova/rag-document-assistant.git
   cd rag-document-assistant
   ```

2. Pull the required Ollama models:
   ```bash
   ollama pull llama3.2
   ollama pull nomic-embed-text
   ```

3. Create a `.env` file:
   ```
   POSTGRES_DB=rag_db
   POSTGRES_USER=rag_user
   POSTGRES_PASSWORD=your_password
   OLLAMA_MODEL=llama3.2
   ```

4. Start the services:
   ```bash
   docker compose up -d
   ```

5. Add a document to the `documents/` folder, then index it:
   ```
   http://localhost:8000/index?filename=your_file.txt
   ```

6. Ask questions:
   ```
   http://localhost:8000/rag?question=Your question here
   ```

## Architecture

```
User -> FastAPI -> RAG:     Chroma (vector search) -> Ollama LLM -> grounded answer
                -> Agent:   LangChain ReAct -> tools -> answer
                -> History: PostgreSQL (SQLAlchemy)
```

## Notes

- The LLM runs locally via Ollama (no API keys, fully private)
- The RAG prompt instructs the model to answer only from the provided context, reducing hallucinations
- Chroma stores document embeddings; PostgreSQL stores query history

---

Built by **Elionora Karimova** — Junior Backend Developer (Python/Django), transitioning into AI development.
