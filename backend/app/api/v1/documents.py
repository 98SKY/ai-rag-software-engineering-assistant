from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
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
from app.services.vector_store import (
    add_embeddings,
    load_index,
    save_index,
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
    Upload a document, extract text, split it into chunks,
    generate embeddings, store vectors in FAISS, and persist
    document/chunk metadata in SQLite.
    """

    # 1. Validate filename
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    # 2. Validate extension
    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, TXT and Markdown files are supported.",
        )

    # 3. Ensure upload directory exists
    ensure_upload_directory()

    # 4. Generate unique document ID
    document_id = str(uuid4())

    stored_filename = f"{document_id}{extension}"
    file_path = UPLOAD_DIR / stored_filename

    try:
        # 5. Read uploaded file
        content = await file.read()

        if not content:
            raise ValueError("Uploaded file is empty.")

        # 6. Save original file
        file_path.write_bytes(content)

        # 7. Extract text
        extracted_text = extract_text(file_path)

        # 8. Clean extracted text
        cleaned_text = clean_text(extracted_text)

        if not cleaned_text:
            raise ValueError(
                "No extractable text found in document."
            )

        # 9. Split text into chunks
        chunks = chunk_text(
            cleaned_text,
            chunk_size=1000,
            chunk_overlap=200,
        )

        if not chunks:
            raise ValueError(
                "Unable to generate chunks from document."
            )

        # 10. Generate embeddings for all chunks
        embeddings = generate_embeddings(chunks)

        if len(embeddings) != len(chunks):
            raise ValueError(
                "Embedding count does not match chunk count."
            )

        # 11. Load existing FAISS index
        faiss_index = load_index()

        # Position where this document's vectors will start
        start_index = faiss_index.ntotal

        # 12. Add embeddings to FAISS
        add_embeddings(
            faiss_index,
            embeddings,
        )

        # 13. Create document database record
        document = Document(
            id=document_id,
            filename=file.filename,
            stored_filename=stored_filename,
            content_type=(
                file.content_type
                or "application/octet-stream"
            ),
            size=len(content),
            characters_extracted=len(cleaned_text),
            chunk_count=len(chunks),
        )

        db.add(document)

        # 14. Create chunk database records
        for index, chunk in enumerate(chunks):
            chunk_record = DocumentChunk(
                id=str(uuid4()),
                document_id=document_id,
                chunk_index=index,
                content=chunk,
                character_count=len(chunk),

                # Map SQLite chunk → FAISS vector
                faiss_index=start_index + index,
            )

            db.add(chunk_record)

        # 15. Save FAISS index
        save_index(faiss_index)

        # 16. Commit SQLite transaction
        db.commit()

    except Exception as exc:
        db.rollback()

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=f"Unable to process document: {str(exc)}",
        ) from exc

    finally:
        await file.close()

    # 17. Return response
    return DocumentResponse(
        document_id=document_id,
        filename=file.filename,
        content_type=(
            file.content_type
            or "application/octet-stream"
        ),
        size=len(content),
        characters_extracted=len(cleaned_text),
        chunk_count=len(chunks),
        message=(
            "Document uploaded, extracted, chunked, "
            "embedded and indexed successfully."
        ),
    )


@router.get("/documents")
def get_documents(
    db: Session = Depends(get_db),
):
    """
    Return all uploaded documents ordered by newest first.
    """

    documents = (
        db.query(Document)
        .order_by(Document.created_at.desc())
        .all()
    )

    return documents


@router.get("/documents/{document_id}/chunks")
def get_document_chunks(
    document_id: str,
    db: Session = Depends(get_db),
):
    """
    Return all chunks belonging to a specific document.
    """

    document = (
        db.query(Document)
        .filter(Document.id == document_id)
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
            DocumentChunk.document_id == document_id
        )
        .order_by(DocumentChunk.chunk_index.asc())
        .all()
    )

    return chunks