from fastapi import FastAPI
from pydantic import BaseModel

from agents import run_agent

app = FastAPI(title="Aulas Python AI")


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(request: ChatRequest):
    resposta = run_agent(request.message)
    return {"response": resposta}