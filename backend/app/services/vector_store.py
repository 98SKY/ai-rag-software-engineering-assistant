from pathlib import Path

import faiss
import numpy as np


VECTOR_DIR = Path("data/vector_store")
INDEX_PATH = VECTOR_DIR / "index.faiss"

EMBEDDING_DIMENSION = 384


def ensure_vector_directory() -> None:
    VECTOR_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


def create_index() -> faiss.Index:
    """
    Create an inner-product FAISS index.

    Because embeddings are normalized, inner product
    behaves like cosine similarity.
    """

    return faiss.IndexFlatIP(EMBEDDING_DIMENSION)


def save_index(index: faiss.Index) -> None:
    ensure_vector_directory()

    faiss.write_index(
        index,
        str(INDEX_PATH),
    )


def load_index() -> faiss.Index:
    ensure_vector_directory()

    if not INDEX_PATH.exists():
        return create_index()

    return faiss.read_index(
        str(INDEX_PATH)
    )


def add_embeddings(
    index: faiss.Index,
    embeddings: np.ndarray,
) -> None:
    if embeddings.size == 0:
        return

    index.add(embeddings)