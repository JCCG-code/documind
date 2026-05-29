from collections.abc import AsyncIterable

import ollama
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from documind.models.query import QueryRequest, QueryResponse
from documind.models.search import SearchResult
from documind.rag.hybrid_retriever import hybrid_search
from documind.rag.rag_agent import run, stream

# API Router Init
router = APIRouter(prefix="/query", tags=["query"])


async def stream_response(
    message: str, rag_results: SearchResult, model: str = "qwen3:8b"
) -> AsyncIterable[str]:
    try:
        # Yield each token
        async for chunk in stream(
            user_message=message, rag_results=rag_results, model=model, think=True
        ):
            yield f"data: {chunk}\n\n"
    except ConnectionError:
        yield "data: [ERROR] Connection error\n\n"
    except ollama.ResponseError as e:
        yield f"data: [ERROR] API error: {e.error} (status: {e.status_code})\n\n"
    except Exception as e:
        yield f"data: [ERROR] Unexpected error: {e}\n\n"
    finally:
        yield "data: [DONE]\n\n"


@router.post("/stream", response_class=StreamingResponse)
async def query_stream(request: QueryRequest):
    # Extracts results
    results = hybrid_search(query=request.text, top_k=5)
    # Filter valid results
    valid_results = [
        result for result in results if result.rerank_score and result.rerank_score > 0
    ]
    if len(valid_results) > 0:
        results_found = SearchResult(
            query=request.text,
            results=valid_results,
            found=True,
            message="Valid results obtained",
        )
    else:
        results_found = SearchResult(
            query=request.text,
            results=valid_results,
            found=False,
            message="No relevant results found",
        )
    # Return streaming response
    if not results_found.found:

        async def no_results():
            yield "data: No relevant information found for your query\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(no_results(), media_type="text/event-stream")
    return StreamingResponse(
        stream_response(
            message=request.text, rag_results=results_found, model=request.model
        ),
        media_type="text/event-stream",
    )


@router.post("/")
async def query(request: QueryRequest) -> QueryResponse:
    # Extracts results
    results = hybrid_search(query=request.text, top_k=5)
    # Filter valid results
    valid_results = [
        result for result in results if result.rerank_score and result.rerank_score > 0
    ]
    if len(valid_results) > 0:
        results_found = SearchResult(
            query=request.text,
            results=valid_results,
            found=True,
            message="Valid results obtained",
        )
    else:
        results_found = SearchResult(
            query=request.text,
            results=valid_results,
            found=False,
            message="No relevant results found",
        )
    # Return streaming response
    if not results_found.found:
        return QueryResponse(
            answer="No relevant information found for your query",
            sources=[],
            confidence=0,
            chunks_used=0,
        )
    return await run(
        user_message=request.text,
        rag_results=results_found,
        model=request.model,
        think=True,
    )
