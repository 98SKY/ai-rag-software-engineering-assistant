from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.rag import (
    AskRequest,
    AskResponse,
    RetrievalMetadata,
    SourceReference,
)
from app.services.rag_service import answer_question


router = APIRouter()


@router.post(
    "/ask",
    response_model=AskResponse,
)
def ask_question(
    request: AskRequest,
    db: Session = Depends(get_db),
) -> AskResponse:

    try:
        result = answer_question(
            question=request.question,
            db=db,
            top_k=request.top_k,
        )

        sources = [
            SourceReference(
                source_number=index,
                chunk_id=chunk.chunk_id,
                document_id=chunk.document_id,
                filename=chunk.filename,
                chunk_index=chunk.chunk_index,
                score=chunk.score,
            )
            for index, chunk in enumerate(
                result.sources,
                start=1,
            )
        ]

        top_score = (
            result.sources[0].score
            if result.sources
            else None
        )

        return AskResponse(
            question=request.question,
            answer=result.answer,
            sources=sources,
            retrieval=RetrievalMetadata(
            top_score=top_score,
            top_k_requested=request.top_k,
            chunks_retrieved=len(result.sources),
            retrieval_time_ms=round(
                result.retrieval_time_ms,
                2,
            ),
            generation_time_ms=round(
                result.generation_time_ms,
                2,
            ),
            total_time_ms=round(
                result.total_time_ms,
                2,
            ),
            ),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to generate answer: {str(exc)}",
        ) from exc