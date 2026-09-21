import os
from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.models.chunk import DocumentChunk
from app.models.document import Document
from app.services.astra_vector_store import (
    semantic_search as astra_semantic_search,
)
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

    vector_store = os.getenv(
        "VECTOR_STORE",
        "faiss",
    ).lower()

    if vector_store == "astra":
        return retrieve_from_astra(
            query=query,
            top_k=top_k,
        )

    if vector_store == "faiss":
        return retrieve_from_faiss(
            query=query,
            db=db,
            top_k=top_k,
        )

    raise ValueError(
        f"Unsupported VECTOR_STORE: {vector_store}"
    )


def retrieve_from_astra(
    query: str,
    top_k: int,
) -> list[RetrievedChunk]:

    query_embedding = generate_embedding(query)

    documents = astra_semantic_search(
        query_embedding=query_embedding,
        top_k=top_k,
    )

    results: list[RetrievedChunk] = []

    for document in documents:
        results.append(
            RetrievedChunk(
                chunk_id=str(document["_id"]),
                document_id=document["document_id"],
                filename=document["filename"],
                chunk_index=document["chunk_index"],
                content=document["content"],
                score=float(
                    document.get("$similarity", 0.0)
                ),
            )
        )

    return results


def retrieve_from_faiss(
    query: str,
    db: Session,
    top_k: int,
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
                Document.id
                == chunk.document_id
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