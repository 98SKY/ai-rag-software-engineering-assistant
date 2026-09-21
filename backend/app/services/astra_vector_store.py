import os
from functools import lru_cache

import numpy as np
from astrapy import DataAPIClient
from dotenv import load_dotenv

load_dotenv()


@lru_cache(maxsize=1)
def get_astra_database():
    token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    endpoint = os.getenv("ASTRA_DB_API_ENDPOINT")

    if not token:
        raise ValueError(
            "ASTRA_DB_APPLICATION_TOKEN is not configured."
        )

    if not endpoint:
        raise ValueError(
            "ASTRA_DB_API_ENDPOINT is not configured."
        )

    client = DataAPIClient(token)

    return client.get_database_by_api_endpoint(
        endpoint
    )


@lru_cache(maxsize=1)
def get_astra_collection():
    collection_name = os.getenv(
        "ASTRA_DB_COLLECTION",
        "software_engineering_chunks",
    )

    database = get_astra_database()

    return database.get_collection(
        collection_name
    )


def insert_chunks(
    chunks: list[dict],
    embeddings: np.ndarray,
) -> None:
    """
    Store chunks and their embeddings in Astra DB.

    Each chunk dictionary must contain:
    chunk_id
    document_id
    filename
    chunk_index
    content
    """

    if len(chunks) != len(embeddings):
        raise ValueError(
            "Chunk count does not match embedding count."
        )

    if not chunks:
        return

    collection = get_astra_collection()

    documents = []

    for chunk, embedding in zip(
        chunks,
        embeddings,
    ):
        documents.append(
            {
                "_id": chunk["chunk_id"],
                "document_id": chunk["document_id"],
                "filename": chunk["filename"],
                "chunk_index": chunk["chunk_index"],
                "content": chunk["content"],
                "$vector": embedding.tolist(),
            }
        )

    collection.insert_many(documents)


def semantic_search(
    query_embedding: np.ndarray,
    top_k: int = 5,
) -> list[dict]:

    collection = get_astra_collection()

    cursor = collection.find(
        {},
        sort={
            "$vector": query_embedding.tolist()
        },
        limit=top_k,
        include_similarity=True,
    )

    return list(cursor)