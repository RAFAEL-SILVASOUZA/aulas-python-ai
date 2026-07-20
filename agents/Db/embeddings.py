import os

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()


URL_EMBEDDINGS = os.getenv("URL_EMBEDDINGS")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")


embeddings = OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    base_url=URL_EMBEDDINGS,
    api_key=os.getenv("API_KEY"),  
    check_embedding_ctx_length=False,
)


def get_vectorstore(collection_name: str = "aulas", persist_directory: str = "chroma_db") -> Chroma:
    """Devolve uma base de vetores Chroma que usa os embeddings do LM Studio."""
    return Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=persist_directory,
    )


def _split_text(text: str, chunk_size: int = 500) -> list[str]:
    """Quebra o texto em pedacos: primeiro por paragrafos, depois por tamanho."""
    chunks: list[str] = []
    for paragrafo in text.split("\n\n"):
        paragrafo = paragrafo.strip()
        if not paragrafo:
            continue

        for i in range(0, len(paragrafo), chunk_size):
            chunks.append(paragrafo[i:i + chunk_size])
    return chunks


def ingest_text(text: str, source: str = "upload") -> int:
    """Quebra o texto em pedacos, gera embeddings e salva na base. Retorna quantos pedacos foram gravados."""
    chunks = _split_text(text)
    if not chunks:
        return 0
    store = get_vectorstore()
    metadados = [{"source": source} for _ in chunks]
    store.add_texts(texts=chunks, metadatas=metadados)
    return len(chunks)


def search(query: str, k: int = 3) -> list[dict]:
    """Busca semantica: retorna os k pedacos mais parecidos com a pergunta."""
    store = get_vectorstore()
    resultados = store.similarity_search_with_score(query, k=k)
    return [
        {
            "texto": doc.page_content,
            "source": doc.metadata.get("source"),
            "score": float(score),
        }
        for doc, score in resultados
    ]