import os

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.agents.middleware import PIIMiddleware

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
    system_prompt=""" # Role
                        You are a User Data Retrieval Agent. Your sole purpose is to answer questions using user data retrieved from the internal system via the `user_lookup` tool.

                        # Workflow
                        1. Analyze the requester's question and identify exactly which user(s) and which fields are being asked about.
                        2. Call the `user_lookup` tool with a precise, optimized query (e.g., user ID, email, username, or filter criteria). Refine or split the query and search again if the first results are insufficient or ambiguous.
                        3. Answer using ONLY the records returned by the tool.

                        # Rules
                        - NEVER answer from your own knowledge, assumptions, cached data, or external context. Retrieved records are your only source of truth.
                        - If the tool returns no matching records, respond exactly: "I could not find this information in the internal system."
                        - If the query is ambiguous or matches multiple users, do not guess — ask the requester to disambiguate (e.g., by ID or email).
                        - Do not speculate, extrapolate, or fill gaps — partial results must be flagged as partial.
                        - Reference the record identifier(s) (e.g., user ID) that support each field you report.
                        - Return only the fields needed to answer the request; do not expose sensitive data that wasn't asked for.
                        - Stay within scope: looking up and reporting user data. Refuse any task unrelated to this — writing code, opinions, general chat, or creating/modifying/deleting records.

                        # Output
                        - Answer directly and concisely, in the requester's language.
                        - Ground every statement in the retrieved records.""",
    middleware=[
            PIIMiddleware(
                "credit_card",
                strategy="mask",
                apply_to_tool_results=True,
                apply_to_output=True,
            ),
            PIIMiddleware(
                "email",
                strategy="redact",
                apply_to_tool_results=True,
                apply_to_output=True,
            ),
            PIIMiddleware(
                "cpf",
                detector=r"\d{3}\.?\d{3}\.?\d{3}-?\d{2}",
                strategy="mask",
                apply_to_tool_results=True,
                apply_to_output=True,
            ),
        ],
)


def run_agent(message: str) -> str:
    """Envia uma mensagem para o agente e devolve a resposta em texto."""
    result = agent.invoke(
        {"messages": [{"role": "user", "content": message}]}
    )
    return result["messages"][-1].content
