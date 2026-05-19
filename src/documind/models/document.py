from pydantic import BaseModel


class Document(BaseModel):
    filename: str
    filepath: str
    size: int
