from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """
    Load the embedding model once and reuse it.
    """
    return SentenceTransformer(MODEL_NAME)


def generate_embedding(text: str) -> np.ndarray:
    """
    Generate a normalized embedding for one piece of text.
    """

    model = get_embedding_model()

    embedding = model.encode(
        text,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    return embedding.astype("float32")


def generate_embeddings(texts: list[str]) -> np.ndarray:
    """
    Generate normalized embeddings for multiple texts.
    """

    if not texts:
        return np.empty((0, 384), dtype="float32")

    model = get_embedding_model()

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    return embeddings.astype("float32")