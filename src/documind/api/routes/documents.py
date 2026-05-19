from fastapi import APIRouter, HTTPException

from documind.models.document import Document
from documind.rag.indexer import index_text

# API Router Init
router = APIRouter(prefix="/documents", tags=["documents"])


SAMPLE_TEXT = """
Python is a high-level programming language. It was created by Guido van Rossum.
Python emphasizes code readability and simplicity.

FastAPI is a modern web framework for Python. It is based on standard Python type hints.
FastAPI is one of the fastest Python frameworks available.

Ollama allows running large language models locally. It supports many open source
models.
Models like Llama, Qwen, and Gemma can run on consumer hardware.
"""


@router.get("")
def get_documents() -> list[Document] | None:
    pass


@router.post("/ingest")
def ingest(request: Document) -> dict:
    points = index_text(
        text=SAMPLE_TEXT, doc_type="plain_text", source="sample_text.txt"
    )
    return {"status": "OK", "points": points}
