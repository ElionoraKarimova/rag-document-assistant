import os
from langchain_ollama import OllamaLLM

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

llm = OllamaLLM(base_url=OLLAMA_HOST, model=OLLAMA_MODEL)


def ask_llm(question: str) -> str:

    return llm.invoke(question)