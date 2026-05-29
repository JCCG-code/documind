import math
from collections.abc import AsyncGenerator, Iterator

from ollama import ChatResponse, chat

from documind.models.query import QueryResponse
from documind.models.search import SearchResult

SYSTEM_INSTRUCTIONS = """You are a code assistant. Don't make things up under any
circumstances. If you don't know something, just say so.
Respond only based on the context provided."""


async def stream(
    user_message: str,
    rag_results: SearchResult,
    model: str = "qwen3:8b",
    think: bool = False,
) -> AsyncGenerator[str, None]:
    # Initializations
    messages: list[dict] = []
    # Creating context str
    context: str = ""
    for result in rag_results.results:
        context += result.text + "\n\n"
    # Create system prompt
    messages.append(
        {"role": "system", "content": f"{SYSTEM_INSTRUCTIONS}\n\nCONTEXT:\n\n{context}"}
    )
    # Create message array
    messages.append({"role": "user", "content": user_message})
    # Chat call streaming mode
    stream: Iterator[ChatResponse] = chat(
        model=model, messages=messages, think=think, stream=True
    )
    thinking = ""
    content = ""
    # Acc partial fields
    for chunk in stream:
        if chunk.message.thinking:
            thinking += chunk.message.thinking
        if chunk.message.content:
            content += chunk.message.content
            yield chunk.message.content
    # Append accumulated fields to the messages
    if thinking or content:
        messages.append(
            {
                "role": "assistant",
                "thinking": thinking,
                "content": content,
            }
        )


async def run(
    user_message: str,
    rag_results: SearchResult,
    model: str = "qwen3:8b",
    think: bool = False,
) -> QueryResponse:
    # Initializations
    messages: list[dict] = []
    # Creating context str, sources and confidence
    context: str = ""
    sources: list[str] = []
    confidence: float = 0
    for result in rag_results.results:
        context += result.text + "\n\n"
        sources.append(result.source)
        if result.rerank_score:
            confidence += result.rerank_score
    confidence = confidence / len(rag_results.results)
    # Deletes repeated
    sources = list(set(sources))
    # Create system prompt
    messages.append(
        {"role": "system", "content": f"{SYSTEM_INSTRUCTIONS}\n\nCONTEXT:\n\n{context}"}
    )
    # Create message array
    messages.append({"role": "user", "content": user_message})
    # Call to model
    response: ChatResponse = chat(model=model, messages=messages, think=think)
    # Return check
    if not response.message.content:
        raise ValueError("Model returned empty response")
    return QueryResponse(
        answer=response.message.content,
        sources=sources,
        # Normalized number to 0 - 1
        confidence=1 / (1 + math.exp(-confidence)),
        chunks_used=len(rag_results.results),
    )
