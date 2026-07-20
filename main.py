from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()


model = ChatOpenAI(
    model="",
    base_url=os.getenv("URL_BASE"), 
    api_key=os.getenv("API_KEY"))

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model=model,    
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)


result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in São Paulo?"}]}
)
print(result["messages"][-1].content_blocks)