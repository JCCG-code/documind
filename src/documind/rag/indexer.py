import uuid
from datetime import datetime

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from documind.rag.chunker import chunk_text
from documind.rag.embeddings import embed

COLLECTION_NAME = "documind"
VECTOR_SIZE = 768


def get_client() -> QdrantClient:
    return QdrantClient(url="http://localhost:6333")


def create_collection(client: QdrantClient) -> None:
    """Create collection if it doesn't exist."""
    # Checks existing collection
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in existing:
        # Creates new collection
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )


def index_text(text: str, doc_type: str, source: str = "unknown") -> int:
    """Chunk, embed and index text into Qdrant. Returns number of chunks indexed."""
    # Creates client and collection
    client = get_client()
    create_collection(client)
    points: list[PointStruct] = []
    # Generates chunks
    chunks_text = chunk_text(text)
    for i, chunk in enumerate(chunks_text):
        # Generates embedding
        embedded_chunk = list(embed(chunk))
        # Point struct to qdrant
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedded_chunk,
                payload={
                    "text": chunk,
                    "source": source,
                    "doc_type": doc_type,
                    "indexed_at": datetime.now(),
                },
            )
        )
    # Insert points
    client.upsert(COLLECTION_NAME, points=points)
    # Return numer of indexed points
    return len(points)
