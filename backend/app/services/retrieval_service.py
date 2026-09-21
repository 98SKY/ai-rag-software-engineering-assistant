from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.models.chunk import DocumentChunk
from app.models.document import Document
from app.services.embedding_service import generate_embedding
from app.services.vector_store import load_index


@dataclass
class RetrievedChunk:
    chunk_id: str
    document_id: str
    filename: str
    chunk_index: int
    content: str
    score: float


def retrieve_chunks(
    query: str,
    db: Session,
    top_k: int = 5,
) -> list[RetrievedChunk]:

    index = load_index()

    if index.ntotal == 0:
        return []

    query_embedding = generate_embedding(
        query
    ).reshape(1, -1)

    search_k = min(
        top_k,
        index.ntotal,
    )

    scores, indices = index.search(
        query_embedding,
        search_k,
    )

    results: list[RetrievedChunk] = []

    for score, faiss_position in zip(
        scores[0],
        indices[0],
    ):
        chunk = (
            db.query(DocumentChunk)
            .filter(
                DocumentChunk.faiss_index
                == int(faiss_position)
            )
            .first()
        )

        if chunk is None:
            continue

        document = (
            db.query(Document)
            .filter(
                Document.id == chunk.document_id
            )
            .first()
        )

        if document is None:
            continue

        results.append(
            RetrievedChunk(
                chunk_id=chunk.id,
                document_id=chunk.document_id,
                filename=document.filename,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
                score=float(score),
            )
        )

    return results