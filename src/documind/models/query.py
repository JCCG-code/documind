from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    text: str
    model: str = Field(default="qwen3:8b")


class QueryResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: float
    chunks_used: int
