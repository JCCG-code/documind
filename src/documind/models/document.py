from pydantic import BaseModel


class Document(BaseModel):
    filename: str
    content_type: str
    size: int
