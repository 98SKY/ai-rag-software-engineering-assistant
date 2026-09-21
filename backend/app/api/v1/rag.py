from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.rag import (
    AskRequest,
    AskResponse,
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
                chunk_id=chunk.chunk_id,
                document_id=chunk.document_id,
                filename=chunk.filename,
                chunk_index=chunk.chunk_index,
                score=chunk.score,
            )
            for chunk in result.sources
        ]

        return AskResponse(
            question=request.question,
            answer=result.answer,
            sources=sources,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to generate answer: {str(exc)}",
        ) from exc