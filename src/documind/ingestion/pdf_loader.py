import io

from fastapi import UploadFile
from pypdf import PdfReader


async def pdf_loader(file: UploadFile) -> str:
    text = ""
    if file.filename:
        # Extract bytes
        content = await file.read()
        reader = PdfReader(io.BytesIO(content))
        # Extract text for each page
        for page in reader.pages:
            text += page.extract_text()
    return text
