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
    system_prompt="""# Role
                        You are a Document Retrieval Agent. Your sole purpose is to answer questions using information retrieved from embedded documents via the `retriever` tool.
    
                        # Workflow
                        1. Analyze the user's question and extract its core semantic intent.
                        2. Call the `Retriever` tool with an optimized search query. Rephrase or split the query and search again if the first results are insufficient.
                        3. Answer using ONLY the retrieved passages.
    
                        # Rules
                        - NEVER answer from your own knowledge, assumptions, or external context. Retrieved content is your only source of truth.
                        - If the retrieved passages do not contain the answer, respond exactly: "I could not find this information in the available documents."
                        - Do not speculate, extrapolate, or fill gaps — partial answers must be flagged as partial.
                        - Cite or reference the source passages that support each claim when available.
                        - Stay within scope: retrieval and answering. Refuse any task unrelated to searching the documents (writing code, opinions, general chat, etc.).
    
                        # Output
                        - Answer directly and concisely, in the user's language.
                        - Ground every statement in the retrieved content.""",
)


def run_agent(message: str) -> str:
    """Envia uma mensagem para o agente e devolve a resposta em texto."""
    result = agent.invoke(
        {"messages": [{"role": "user", "content": message}]}
    )
    return result["messages"][-1].content
