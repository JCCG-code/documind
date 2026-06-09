from fastapi import APIRouter, HTTPException, UploadFile

from documind.ingestion.file_dispatcher import load_file, load_indexed
from documind.models.document import Document

# API Router Init
router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("")
def get_documents() -> list[Document] | None:
    return load_indexed()


@router.post("/ingest")
async def ingest(file: UploadFile) -> dict:
    try:
        return await load_file(file)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error while indexing file {file.filename}: {e}"
        )
