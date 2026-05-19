from fastapi import APIRouter, HTTPException

from documind.models.document import Document

# API Router Init
router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("")
def get_documents() -> list[Document] | None:
    pass


@router.post("/ingest")
def ingest(request: Document) -> dict:
    return {"status": "OK"}
