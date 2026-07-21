from io import BytesIO
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel

from agents import run_agent
from agents.Db import ingest_text

from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import DocumentStream

app = FastAPI(title="Aulas Python AI")

converter = DocumentConverter()
FORMATOS_ACEITOS = (".pdf", ".docx", ".pptx", ".xlsx", ".html", ".md", ".txt")

class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(request: ChatRequest):
    resposta = run_agent(request.message)
    return {"response": resposta}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(FORMATOS_ACEITOS):
        raise HTTPException(
            status_code=400,
            detail=f"Formato não suportado. Use: {', '.join(FORMATOS_ACEITOS)}",
        )

    dados = await file.read()

    # docling é síncrono e pesado (CPU/modelos) -> tira do event loop
    source = DocumentStream(name=file.filename, stream=BytesIO(dados))
    result = await run_in_threadpool(converter.convert, source)

    # Documento estruturado -> Markdown (é o "texto" que você já ingere)
    conteudo = result.document.export_to_markdown()

    quantidade = ingest_text(conteudo, source=file.filename)
    return {"arquivo": file.filename, "pedacos_gravados": quantidade}