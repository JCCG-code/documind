from collections.abc import Sequence

from ollama import embeddings


def embed(text: str, model: str = "nomic-embed-text") -> Sequence[float]:
    """Allows to convert texts to vectors"""
    result = embeddings(model=model, prompt=text)
    return result.embedding
