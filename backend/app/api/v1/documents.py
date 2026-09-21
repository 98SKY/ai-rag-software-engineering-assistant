from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.chunk import DocumentChunk
from app.models.document import Document
from app.schemas.document import DocumentResponse
from app.services.document_service import (
    ALLOWED_EXTENSIONS,
    UPLOAD_DIR,
    chunk_text,
    clean_text,
    ensure_upload_directory,
    extract_text,
)
from app.services.embedding_service import generate_embeddings
from app.services.vector_store_factory import (
    get_vector_store_name,
    index_chunks,
)


router = APIRouter()


@router.post(
    "/documents/upload",
    response_model=DocumentResponse,
)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> DocumentResponse:
    """
    Upload and process a document.

    Pipeline:
    1. Validate the uploaded file.
    2. Save the original document.
    3. Extract and clean text.
    4. Split text into chunks.
    5. Generate embeddings.
    6. Index chunks in the configured vector store.
    7. Persist document/chunk metadata in SQLite.

    Supported vector stores:
    - FAISS
    - Astra DB
    """

    # --------------------------------------------------
    # 1. Validate filename
    # --------------------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    # --------------------------------------------------
    # 2. Validate extension
    # --------------------------------------------------

    extension = Path(
        file.filename
    ).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Only PDF, TXT and Markdown "
                "files are supported."
            ),
        )

    # --------------------------------------------------
    # 3. Ensure document storage directory exists
    # --------------------------------------------------

    ensure_upload_directory()

    # --------------------------------------------------
    # 4. Generate document identifiers
    # --------------------------------------------------

    document_id = str(uuid4())

    stored_filename = (
        f"{document_id}{extension}"
    )

    file_path = (
        UPLOAD_DIR / stored_filename
    )

    # Variables used when building the final response.
    content: bytes = b""
    cleaned_text = ""
    chunks: list[str] = []

    try:
        # --------------------------------------------------
        # 5. Read uploaded file
        # --------------------------------------------------

        content = await file.read()

        if not content:
            raise ValueError(
                "Uploaded file is empty."
            )

        # --------------------------------------------------
        # 6. Save original document
        # --------------------------------------------------

        file_path.write_bytes(content)

        # --------------------------------------------------
        # 7. Extract text
        # --------------------------------------------------

        extracted_text = extract_text(
            file_path
        )

        # --------------------------------------------------
        # 8. Clean extracted text
        # --------------------------------------------------

        cleaned_text = clean_text(
            extracted_text
        )

        if not cleaned_text:
            raise ValueError(
                "No extractable text found "
                "in document."
            )

        # --------------------------------------------------
        # 9. Split document into chunks
        # --------------------------------------------------

        chunks = chunk_text(
            cleaned_text,
            chunk_size=1000,
            chunk_overlap=200,
        )

        if not chunks:
            raise ValueError(
                "Unable to generate chunks "
                "from document."
            )

        # --------------------------------------------------
        # 10. Generate embeddings
        # --------------------------------------------------

        embeddings = generate_embeddings(
            chunks
        )

        if len(embeddings) != len(chunks):
            raise ValueError(
                "Embedding count does not "
                "match chunk count."
            )

        # --------------------------------------------------
        # 11. Generate chunk IDs BEFORE vector indexing
        #
        # This is important for Astra because the chunk UUID
        # becomes the Astra document _id.
        # --------------------------------------------------

        chunk_data: list[dict] = []

        for index, chunk in enumerate(
            chunks
        ):
            chunk_data.append(
                {
                    "chunk_id": str(uuid4()),
                    "document_id": document_id,
                    "filename": file.filename,
                    "chunk_index": index,
                    "content": chunk,
                }
            )

        # --------------------------------------------------
        # 12. Index vectors
        #
        # VECTOR_STORE=faiss
        #     -> vectors are stored in FAISS
        #     -> returns FAISS positions
        #
        # VECTOR_STORE=astra
        #     -> vectors + metadata are stored in Astra
        #     -> returns None for each FAISS position
        # --------------------------------------------------

        vector_store_name = (
            get_vector_store_name()
        )

        vector_positions = index_chunks(
            chunks=chunk_data,
            embeddings=embeddings,
        )

        if (
            len(vector_positions)
            != len(chunk_data)
        ):
            raise ValueError(
                "Vector position count does "
                "not match chunk count."
            )

        # --------------------------------------------------
        # 13. Create document database record
        # --------------------------------------------------

        document = Document(
            id=document_id,
            filename=file.filename,
            stored_filename=stored_filename,
            content_type=(
                file.content_type
                or "application/octet-stream"
            ),
            size=len(content),
            characters_extracted=len(
                cleaned_text
            ),
            chunk_count=len(chunks),
        )

        db.add(document)

        # --------------------------------------------------
        # 14. Create SQLite chunk records
        # --------------------------------------------------

        for (
            current_chunk,
            vector_position,
        ) in zip(
            chunk_data,
            vector_positions,
        ):
            chunk_record = DocumentChunk(
                id=current_chunk["chunk_id"],
                document_id=document_id,
                chunk_index=current_chunk[
                    "chunk_index"
                ],
                content=current_chunk[
                    "content"
                ],
                character_count=len(
                    current_chunk["content"]
                ),

                # FAISS:
                #     0, 1, 2, ...
                #
                # Astra:
                #     None
                faiss_index=vector_position,
            )

            db.add(chunk_record)

        # --------------------------------------------------
        # 15. Commit SQLite transaction
        # --------------------------------------------------

        db.commit()

    except Exception as exc:
        # Roll back SQLite changes.
        db.rollback()

        # Remove uploaded file if processing failed.
        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to process document: "
                f"{str(exc)}"
            ),
        ) from exc

    finally:
        await file.close()

    # --------------------------------------------------
    # 16. Return upload response
    # --------------------------------------------------

    return DocumentResponse(
        document_id=document_id,
        filename=file.filename,
        content_type=(
            file.content_type
            or "application/octet-stream"
        ),
        size=len(content),
        characters_extracted=len(
            cleaned_text
        ),
        chunk_count=len(chunks),
        message=(
            "Document uploaded, extracted, "
            "chunked, embedded and indexed "
            f"successfully using "
            f"{vector_store_name.upper()}."
        ),
    )


@router.get("/documents")
def get_documents(
    db: Session = Depends(get_db),
):
    """
    Return all uploaded documents,
    ordered newest first.
    """

    documents = (
        db.query(Document)
        .order_by(
            Document.created_at.desc()
        )
        .all()
    )

    return documents


@router.get(
    "/documents/{document_id}/chunks"
)
def get_document_chunks(
    document_id: str,
    db: Session = Depends(get_db),
):
    """
    Return all chunks belonging to
    a specific document.
    """

    document = (
        db.query(Document)
        .filter(
            Document.id == document_id
        )
        .first()
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    chunks = (
        db.query(DocumentChunk)
        .filter(
            DocumentChunk.document_id
            == document_id
        )
        .order_by(
            DocumentChunk.chunk_index.asc()
        )
        .all()
    )

    return chunks