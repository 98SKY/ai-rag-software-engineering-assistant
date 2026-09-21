from app.services.embedding_service import generate_embedding


text = "Spring Boot is used for building Java microservices."

embedding = generate_embedding(text)

print("Shape:", embedding.shape)
print("First 10 values:", embedding[:10])