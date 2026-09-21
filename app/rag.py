import os
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")
CHROMA_HOST = os.getenv("CHROMA_HOST", "chroma")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))


embeddings = OllamaEmbeddings(
    base_url=OLLAMA_HOST,
    model="nomic-embed-text",
)


def get_vectorstore():
    import chromadb
    client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    return Chroma(
        client=client,
        collection_name="documents",
        embedding_function=embeddings,
    )


def index_document(file_path: str):

    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    chunks = splitter.split_documents(documents)

    vectorstore = get_vectorstore()
    vectorstore.add_documents(chunks)

    return len(chunks)
def ask_with_rag(question: str) -> dict:
    from app.llm import llm
    vectorstore = get_vectorstore()
    results = vectorstore.similarity_search(question, k=3)
    context = "\n\n".join([doc.page_content for doc in results])
    prompt = f"""Ответь на вопрос, используя только информацию из контекста ниже.
    Если ответа нет в контексте, скажи, что информации недостаточно.

    Контекст:
    {context}

    Вопрос: {question}

    Ответ:"""
    answer = llm.invoke(prompt)

    return {
        "question": question,
        "answer": answer,
        "sources_found": len(results),
    }