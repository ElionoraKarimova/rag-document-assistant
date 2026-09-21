from fastapi import FastAPI
from app.llm import ask_llm
from app.rag import index_document, ask_with_rag
from app.agent import ask_agent

app = FastAPI(title="RAG Document Assistant")


@app.get("/")
def root():
    return {"message": "RAG Document Assistant is running!"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ask")
def ask(question: str):
    
    answer = ask_llm(question)
    return {"question": question, "answer": answer}

@app.get("/index")
def index(filename: str):
    file_path = f"documents/{filename}"
    chunks_count = index_document(file_path)
    return {"filename": filename, "chunks_indexed": chunks_count}
@app.get("/rag")
def rag(question: str):
    return ask_with_rag(question)

@app.get("/agent")
def agent_endpoint(question: str):
    """Задать вопрос AI-агенту (сам выбирает инструменты)."""
    return ask_agent(question)