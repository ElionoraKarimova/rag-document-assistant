from fastapi import FastAPI
from app.llm import ask_llm
from app.rag import index_document, ask_with_rag
from app.agent import ask_agent
from app.database import engine, get_db
from app.models import Base, QueryHistory
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import UploadFile, File
import shutil
import os
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="RAG Document Assistant")
Base.metadata.create_all(bind=engine)

@app.get("/", response_class=HTMLResponse)
def root():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()


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
def rag(question: str, db: Session = Depends(get_db)):
    result = ask_with_rag(question)
    record = QueryHistory(
        question=question,
        answer=result["answer"],
        mode="rag",
    )
    db.add(record)
    db.commit()
    return result

@app.get("/agent")
def agent_endpoint(question: str, db: Session = Depends(get_db)):
    result = ask_agent(question)
    record = QueryHistory(
        question=question,
        answer=result["answer"],
        mode="agent",
    )
    db.add(record)
    db.commit()
    return result
@app.get("/history")
def history(db: Session = Depends(get_db)):
    records = db.query(QueryHistory).order_by(QueryHistory.created_at.desc()).all()
    return [
        {
            "id": r.id,
            "question": r.question,
            "answer": r.answer,
            "mode": r.mode,
            "created_at": r.created_at.isoformat(),
        }
        for r in records
    ]
@app.post("/upload")
def upload_document(file: UploadFile = File(...)):
    os.makedirs("documents", exist_ok=True)

    file_path = f"documents/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    chunks_count = index_document(file_path)

    return {
        "filename": file.filename,
        "status": "uploaded and indexed",
        "chunks_indexed": chunks_count,
    }