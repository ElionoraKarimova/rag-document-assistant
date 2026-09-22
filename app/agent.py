import os
from langchain_ollama import ChatOllama
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain_core.prompts import PromptTemplate
from app.rag import get_vectorstore

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

# LLM для агента (Chat-версия)
chat_llm = ChatOllama(base_url=OLLAMA_HOST, model=OLLAMA_MODEL, temperature=0)


def search_documents(query: str) -> str:

    vectorstore = get_vectorstore()
    results = vectorstore.similarity_search(query, k=3)
    if not results:
        return "В документах ничего не найдено."
    return "\n\n".join([doc.page_content for doc in results])


# Набор инструментов агента
tools = [
    Tool(
        name="search_documents",
        func=search_documents,
        description="Полезно для поиска информации в документах компании. "
                    "Используй, когда вопрос про компанию, услуги, врачей, расписание и т.д.",
    ),
]


prompt = PromptTemplate.from_template("""Answer the following question as best you can. Respond in the same language as the question, in a friendly and conversational tone. You have access to these tools:

{tools}

Используй формат:
Question: вопрос, на который надо ответить
Thought: подумай, что делать
Action: название инструмента, одно из [{tool_names}]
Action Input: входные данные для инструмента
Observation: результат инструмента
... (Thought/Action/Action Input/Observation могут повторяться)
Thought: теперь я знаю ответ
Final Answer: финальный ответ на вопрос

Начинай!

Question: {input}
Thought:{agent_scratchpad}""")


agent = create_react_agent(chat_llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=10,
)


def ask_agent(question: str) -> dict:

    result = agent_executor.invoke({"input": question})
    return {
        "question": question,
        "answer": result["output"],
    }