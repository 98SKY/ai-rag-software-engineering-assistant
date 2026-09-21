import os

from astrapy.info import (
    CollectionDefinition,
    CollectionVectorOptions,
)
from astrapy.constants import VectorMetric
from dotenv import load_dotenv

from app.services.astra_vector_store import get_astra_database

load_dotenv()

database = get_astra_database()

collection_name = os.getenv(
    "ASTRA_DB_COLLECTION",
    "software_engineering_chunks",
)

existing_collections = database.list_collection_names()

if collection_name in existing_collections:
    print(
        f"Collection already exists: {collection_name}"
    )
else:
    database.create_collection(
        collection_name,
        definition=CollectionDefinition(
            vector=CollectionVectorOptions(
                dimension=384,
                metric=VectorMetric.COSINE,
            ),
        ),
    )

    print(
        f"Collection created successfully: {collection_name}"
    )