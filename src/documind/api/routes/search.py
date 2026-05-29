from fastapi import APIRouter, HTTPException

from documind.models.search import SearchResult
from documind.rag.hybrid_retriever import hybrid_search

# API Router Init
router = APIRouter(prefix="/search", tags=["search"])


@router.get("")
async def search(query: str) -> SearchResult:
    try:
        results = hybrid_search(query=query, top_k=3)
        valid_results = [
            result
            for result in results
            if result.rerank_score and result.rerank_score > 0
        ]
        if len(valid_results) > 0:
            return SearchResult(
                query=query,
                results=valid_results,
                found=True,
                message="Valid results obtained",
            )
        else:
            return SearchResult(
                query=query,
                results=valid_results,
                found=False,
                message="No relevant results found",
            )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error while searching query: {query}.\nError -> {e}",
        )
