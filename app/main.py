from fastapi import FastAPI
from app.llm import ask_llm

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