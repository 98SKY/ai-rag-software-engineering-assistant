from app.core.database import SessionLocal
from app.models.chunk import DocumentChunk
from app.models.document import Document
from app.services.astra_vector_store import insert_chunks
from app.services.embedding_service import generate_embeddings


def main():
    db = SessionLocal()

    try:
        chunks = (
            db.query(DocumentChunk)
            .order_by(
                DocumentChunk.document_id,
                DocumentChunk.chunk_index,
            )
            .all()
        )

        if not chunks:
            print("No chunks found in SQLite.")
            return

        astra_chunks = []
        texts = []

        for chunk in chunks:
            document = (
                db.query(Document)
                .filter(
                    Document.id == chunk.document_id
                )
                .first()
            )

            if document is None:
                continue

            astra_chunks.append(
                {
                    "chunk_id": chunk.id,
                    "document_id": chunk.document_id,
                    "filename": document.filename,
                    "chunk_index": chunk.chunk_index,
                    "content": chunk.content,
                }
            )

            texts.append(chunk.content)

        if not astra_chunks:
            print("No valid chunks found.")
            return

        print(
            f"Generating embeddings for "
            f"{len(texts)} chunks..."
        )

        embeddings = generate_embeddings(texts)

        print(
            f"Embedding shape: {embeddings.shape}"
        )

        print("Uploading chunks to Astra DB...")

        insert_chunks(
            chunks=astra_chunks,
            embeddings=embeddings,
        )

        print(
            f"Successfully indexed "
            f"{len(astra_chunks)} chunks into Astra DB."
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()