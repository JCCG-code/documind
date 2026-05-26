import hashlib
import json
from pathlib import Path

from fastapi import HTTPException, UploadFile

from documind.ingestion.md_loader import markdown_loader
from documind.ingestion.pdf_loader import pdf_loader
from documind.ingestion.txt_loader import plain_loader
from documind.rag.indexer import index_text

INDEXED_FILE = Path("indexed_files.json")


async def load_file(file: UploadFile) -> dict:
    try:
        if file.filename and file.content_type and file.size:
            # Extract hash file
            content = await file.read()
            hash = hashlib.sha256(content).hexdigest()
            # Checks hash
            if is_indexed(hash=hash):
                raise HTTPException(
                    status_code=409, detail=f"File {file.filename} already indexed"
                )
            # Indexing new file
            await file.seek(0)
            if file.content_type == "text/markdown":
                text = await markdown_loader(file)
            elif file.content_type == "text/plain":
                text = await plain_loader(file)
            elif file.content_type == "application/pdf":
                text = await pdf_loader(file)
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"File type of {file.filename} not supported",
                )
            # Index text in QDrant
            points = index_text(
                text=text, doc_type=file.content_type, source=file.filename
            )
            # Save or update indexed_files
            save_indexed(filename=file.filename, hash=hash)
            return {"status": "OK", "points": points}
        return {"status": "FAILED", "details": "File not detected"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error reading the file {file.filename}: {e}"
        )
    finally:
        await file.close()


def load_indexed() -> dict:
    if not INDEXED_FILE.exists():
        return {}
    return json.loads(INDEXED_FILE.read_text())


def is_indexed(hash: str) -> bool:
    return hash in load_indexed().values()


def save_indexed(filename: str, hash: str) -> None:
    data = load_indexed()
    data[filename] = hash
    INDEXED_FILE.write_text(json.dumps(data, indent=2))
