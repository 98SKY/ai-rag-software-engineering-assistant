from pydantic import BaseModel


class ChunkResponse(BaseModel):
    chunk_id: str
    chunk_index: int
    content: str
    character_count: int


class DocumentResponse(BaseModel):
    document_id: str
    filename: str
    content_type: str
    size: int
    characters_extracted: int
    chunk_count: int
    message: str