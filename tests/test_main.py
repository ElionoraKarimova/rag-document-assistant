from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_history_returns_list():
    response = client.get("/history")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_ask_requires_question():
    response = client.get("/ask")
    assert response.status_code == 422

import pytest

def test_ask_llm_returns_answer():
    response = client.get("/ask", params={"question": "Say hello"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert len(data["answer"]) > 0


def test_index_document():
    response = client.get("/index", params={"filename": "sample.txt"})
    assert response.status_code == 200
    data = response.json()
    assert "chunks_indexed" in data
    assert data["chunks_indexed"] > 0


def test_rag_returns_answer_with_sources():
    response = client.get("/rag", params={"question": "What is this about?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources_found" in data
    assert len(data["answer"]) > 0


def test_history_saves_query():
    client.get("/rag", params={"question": "Test question for history"})
    response = client.get("/history")
    assert response.status_code == 200
    history = response.json()
    assert len(history) > 0  
    assert "question" in history[0]
    assert "answer" in history[0]
    assert "mode" in history[0]