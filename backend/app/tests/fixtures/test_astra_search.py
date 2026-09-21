from app.services.astra_vector_store import semantic_search
from app.services.embedding_service import generate_embedding


question = (
    "Does this candidate have experience "
    "building scalable backend systems?"
)

embedding = generate_embedding(question)

results = semantic_search(
    query_embedding=embedding,
    top_k=5,
)

print(f"Results: {len(results)}")

for index, result in enumerate(
    results,
    start=1,
):
    print()
    print("=" * 60)
    print(f"Result {index}")
    print(f"Filename: {result.get('filename')}")
    print(f"Chunk: {result.get('chunk_index')}")
    print(
        f"Similarity: "
        f"{result.get('$similarity')}"
    )
    print()
    print(result.get("content", "")[:500])