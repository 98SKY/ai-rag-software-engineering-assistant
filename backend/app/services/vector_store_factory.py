import os

import numpy as np

from app.services.astra_vector_store import (
    insert_chunks,
)
from app.services.vector_store import (
    add_embeddings,
    load_index,
    save_index,
)


SUPPORTED_VECTOR_STORES = {
    "faiss",
    "astra",
}


def get_vector_store_name() -> str:
    """
    Return the configured vector-store name.

    Defaults to FAISS when VECTOR_STORE
    is not specified.
    """

    vector_store = os.getenv(
        "VECTOR_STORE",
        "faiss",
    ).strip().lower()

    if (
        vector_store
        not in SUPPORTED_VECTOR_STORES
    ):
        raise ValueError(
            "Unsupported VECTOR_STORE: "
            f"{vector_store}. "
            "Supported values are: "
            "faiss, astra."
        )

    return vector_store


def index_chunks(
    chunks: list[dict],
    embeddings: np.ndarray,
) -> list[int | None]:
    """
    Index chunks in the configured
    vector store.

    Returns:
        FAISS:
            List of vector positions.

        Astra:
            List containing None because
            Astra uses chunk UUIDs rather
            than positional indexes.
    """

    if len(chunks) != len(embeddings):
        raise ValueError(
            "Chunk count does not match "
            "embedding count."
        )

    if not chunks:
        return []

    vector_store = (
        get_vector_store_name()
    )

    # --------------------------------------------------
    # Astra DB
    # --------------------------------------------------

    if vector_store == "astra":
        insert_chunks(
            chunks=chunks,
            embeddings=embeddings,
        )

        return [
            None
            for _ in chunks
        ]

    # --------------------------------------------------
    # FAISS
    # --------------------------------------------------

    faiss_index = load_index()

    start_index = (
        faiss_index.ntotal
    )

    add_embeddings(
        faiss_index,
        embeddings,
    )

    save_index(
        faiss_index
    )

    return [
        start_index + index
        for index in range(
            len(chunks)
        )
    ]