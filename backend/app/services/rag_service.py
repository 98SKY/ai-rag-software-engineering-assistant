from dataclasses import dataclass
from time import perf_counter

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
    retrieval_time_ms: float
    generation_time_ms: float
    total_time_ms: float


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
[Source {number}]
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

    total_start = perf_counter()

    retrieval_start = perf_counter()

    chunks = retrieve_chunks(
        query=question,
        db=db,
        top_k=top_k,
    )

    retrieval_time_ms = (
        perf_counter() - retrieval_start
    ) * 1000

    if not chunks:
        total_time_ms = (
            perf_counter() - total_start
        ) * 1000

        return RAGResult(
            answer=(
                "I could not find relevant information "
                "in the indexed documents."
            ),
            sources=[],
            retrieval_time_ms=retrieval_time_ms,
            generation_time_ms=0.0,
            total_time_ms=total_time_ms,
        )

    context = build_context(chunks)

    generation_start = perf_counter()

    answer = generate_answer(
        question=question,
        context=context,
    )

    generation_time_ms = (
        perf_counter() - generation_start
    ) * 1000

    total_time_ms = (
        perf_counter() - total_start
    ) * 1000

    return RAGResult(
        answer=answer,
        sources=chunks,
        retrieval_time_ms=retrieval_time_ms,
        generation_time_ms=generation_time_ms,
        total_time_ms=total_time_ms,
    )