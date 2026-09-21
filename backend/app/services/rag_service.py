from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.services.llm_service import generate_answer
from app.services.retrieval_service import (
    RetrievedChunk,
    retrieve_chunks,
)


@dataclass
class RAGResult:
    answer: str
    sources: list[RetrievedChunk]


def build_context(
    chunks: list[RetrievedChunk],
) -> str:
    sections: list[str] = []

    for number, chunk in enumerate(
        chunks,
        start=1,
    ):
        sections.append(
            f"""
[SOURCE {number}]
File: {chunk.filename}
Chunk: {chunk.chunk_index}

{chunk.content}
""".strip()
        )

    return "\n\n".join(sections)


def answer_question(
    question: str,
    db: Session,
    top_k: int = 5,
) -> RAGResult:

    chunks = retrieve_chunks(
        query=question,
        db=db,
        top_k=top_k,
    )

    if not chunks:
        return RAGResult(
            answer=(
                "I could not find relevant information "
                "in the indexed documents."
            ),
            sources=[],
        )

    context = build_context(chunks)

    answer = generate_answer(
        question=question,
        context=context,
    )

    return RAGResult(
        answer=answer,
        sources=chunks,
    )