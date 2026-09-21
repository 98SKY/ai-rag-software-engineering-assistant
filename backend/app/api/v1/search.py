from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.search import (
    SearchRequest,
    SearchResponse,
    SearchResult,
)
from app.services.retrieval_service import retrieve_chunks


router = APIRouter()


@router.post(
    "/search",
    response_model=SearchResponse,
)
def semantic_search(
    request: SearchRequest,
    db: Session = Depends(get_db),
) -> SearchResponse:

    chunks = retrieve_chunks(
        query=request.query,
        db=db,
        top_k=request.top_k,
    )

    if not chunks:
        raise HTTPException(
            status_code=400,
            detail="No indexed documents available.",
        )

    results = [
        SearchResult(
            chunk_id=chunk.chunk_id,
            document_id=chunk.document_id,
            filename=chunk.filename,
            chunk_index=chunk.chunk_index,
            content=chunk.content,
            score=chunk.score,
        )
        for chunk in chunks
    ]

    return SearchResponse(
        query=request.query,
        results=results,
    )