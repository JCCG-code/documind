from pydantic import BaseModel


class Result(BaseModel):
    text: str
    source: str
    doc_type: str
    score: float
    rrf_score: float
    rerank_score: float | None = None


class SearchResult(BaseModel):
    query: str
    results: list[Result]
    found: bool
    message: str
