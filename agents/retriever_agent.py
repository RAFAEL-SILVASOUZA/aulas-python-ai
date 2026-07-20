import os

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from agents.Db import search


load_dotenv()


model = ChatOpenAI(
    model="",
    base_url=os.getenv("URL_BASE"),
    api_key=os.getenv("API_KEY"),
)


def retriever(query: str, k: int) -> str:
    """Search for documents matching a query.

    Args:
        query: The search string.
        k: Number of results to return.

    Returns:
        A dict with the original query and the list of results.
    """
    resultados = search(query, k=k)
    return {"query": query, "resultados": resultados}


agent = create_agent(
    model=model,
    tools=[retriever],
    system_prompt="You are a helpful assistant",
)


def run_agent(message: str) -> str:
    """Envia uma mensagem para o agente e devolve a resposta em texto."""
    result = agent.invoke(
        {"messages": [{"role": "user", "content": message}]}
    )
    return result["messages"][-1].content
