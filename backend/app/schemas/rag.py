from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(
        min_length=2,
        max_length=2000,
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=10,
    )


class SourceReference(BaseModel):
    chunk_id: str
    document_id: str
    filename: str
    chunk_index: int
    score: float


class AskResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceReference]