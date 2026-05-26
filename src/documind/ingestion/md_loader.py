from fastapi import UploadFile


async def markdown_loader(file: UploadFile) -> str:
    # Get file in bytes
    content = await file.read()
    # Transform to string
    return content.decode(encoding="utf-8")
