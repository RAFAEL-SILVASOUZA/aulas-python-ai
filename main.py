from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel

from agents import run_agent
from agents.Db import ingest_text

app = FastAPI(title="Aulas Python AI")


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(request: ChatRequest):
    resposta = run_agent(request.message)
    return {"response": resposta}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Envie um arquivo .txt")

    conteudo = (await file.read()).decode("utf-8")
    quantidade = ingest_text(conteudo, source=file.filename)

    return {"arquivo": file.filename, "pedacos_gravados": quantidade}