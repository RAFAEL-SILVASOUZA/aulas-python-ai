# Aulas Python AI

Mini curso de construção de uma **API de IA com FastAPI + LangChain**, usando um
modelo local servido pelo **LM Studio** (compatível com a API da OpenAI).

Ao longo das aulas saímos de um script simples de agente até uma API com
**RAG** (busca semântica em uma base de embeddings).

---

## O que o projeto faz

- Sobe uma API FastAPI com dois endpoints.
- Conversa com um **agente LangChain** que tem uma _tool_ de busca (retriever).
- Recebe um arquivo `.txt`, quebra em pedaços, gera **embeddings** e guarda numa
  base vetorial **Chroma**.
- Responde perguntas usando os trechos mais relevantes da base (busca semântica).

Todos os modelos (chat e embeddings) rodam **localmente no LM Studio** — não é
usada nenhuma nuvem paga.

---

## Estrutura

```
aulas-python-ai/
├── main.py                     # API FastAPI (endpoints /chat e /upload)
├── agents/
│   ├── __init__.py             # expõe run_agent
│   ├── retriever_agent.py      # agente LangChain + tool de busca (retriever)
│   └── Db/
│       ├── __init__.py         # expõe embeddings, get_vectorstore, ingest_text, search
│       └── embeddings.py       # embeddings do LM Studio + base Chroma + ingestão/busca
├── requirements.txt
└── .env                        # não versionado (ver abaixo)
```

---

## Pré-requisitos

- Python 3.10+
- [LM Studio](https://lmstudio.ai/) rodando o servidor local
- Dois modelos carregados no LM Studio:
  - **Chat** — qualquer modelo instruct (ex.: um Llama/Qwen instruct)
  - **Embeddings** — `nomic-ai/nomic-embed-text-v1.5-GGUF`
    (aparece como `text-embedding-nomic-embed-text-v1.5`).
    Para textos em português, `BAAI/bge-m3` é uma boa alternativa.

> O servidor do LM Studio deste projeto está configurado na porta **4321**.

---

## Configuração

1. Crie e ative um ambiente virtual e instale as dependências:

   ```bash
   python -m venv .venv
   .venv/Scripts/activate      # Windows
   pip install -r requirements.txt
   ```

2. Crie um arquivo `.env` na raiz:

   ```env
   # modelo de CHAT (LM Studio)
   URL_BASE=http://localhost:4321/v1
   API_KEY=lm-studio

   # modelo de EMBEDDINGS (LM Studio)
   URL_EMBEDDINGS=http://localhost:4321/v1
   EMBEDDING_MODEL=text-embedding-nomic-embed-text-v1.5
   ```

   > A `API_KEY` pode ser qualquer texto — o LM Studio a ignora, mas o cliente
   > exige que exista.

3. No LM Studio, carregue os modelos de chat e de embeddings e **inicie o
   servidor** na porta `4321`.

---

## Como rodar

```bash
.venv/Scripts/uvicorn main:app --reload
```

Abra a documentação interativa em **http://127.0.0.1:8000/docs**.

### Endpoints

| Método | Rota      | O que faz                                                        |
|--------|-----------|------------------------------------------------------------------|
| `POST` | `/chat`   | Envia uma mensagem para o agente e recebe a resposta.            |
| `POST` | `/upload` | Recebe um `.txt`, gera embeddings e grava na base Chroma.        |

**Enviar dados para a base:**

```bash
curl -X POST http://127.0.0.1:8000/upload -F "file=@dados.txt"
```

**Conversar com o agente (ele usa a base via a tool de busca):**

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "O que os documentos dizem sobre X?"}'
```

---

## Roteiro das aulas (pelos commits)

O histórico do Git segue a progressão do curso — cada commit é uma aula:

| Commit    | Aula      | Conteúdo                                                                 |
|-----------|-----------|--------------------------------------------------------------------------|
| `initial` | Aula 01   | Setup do projeto: `.gitignore` e `requirements.txt`.                     |
| `aula-02` | Aula 02   | Primeiro agente LangChain rodando como script (`main.py`).              |
| `aula-03` | Aula 03   | Refatoração: pacote `agents/` e transformação em **API FastAPI**.       |
| `aula-04` | Aula 04   | Módulo `Db` com **embeddings + Chroma**, endpoint `/upload` e a tool de busca (**RAG**) no agente. |

---

## Observações

- A base vetorial é persistida na pasta `chroma_db/` (criada na primeira
  ingestão).
- Os endpoints dependem do LM Studio ligado: `/chat` precisa do modelo de chat e
  `/upload` do modelo de embeddings carregados.
