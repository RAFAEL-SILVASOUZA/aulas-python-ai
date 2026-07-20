import os

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


model = ChatOpenAI(
    model="",
    base_url=os.getenv("URL_BASE"),
    api_key=os.getenv("API_KEY"),
)


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)


def run_agent(message: str) -> str:
    """Envia uma mensagem para o agente e devolve a resposta em texto."""
    result = agent.invoke(
        {"messages": [{"role": "user", "content": message}]}
    )
    return result["messages"][-1].content
