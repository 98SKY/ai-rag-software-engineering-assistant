from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(
        min_length=2,
        max_length=1000,
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
    )


class SearchResult(BaseModel):
    chunk_id: str
    document_id: str
    filename: str
    chunk_index: int
    content: str
    score: float


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]