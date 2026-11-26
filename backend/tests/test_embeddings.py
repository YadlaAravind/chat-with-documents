
from app.services.embedding_service import generate_embeddings


sample_chunks = [
    {
        "chunk_id": 1,
        "page_number": 1,
        "chunk_index": 1,
        "content": "Python is a programming language."
    },
    {
        "chunk_id": 2,
        "page_number": 1,
        "chunk_index": 2,
        "content": "Flask is a Python web framework."
    },
    {
        "chunk_id": 3,
        "page_number": 2,
        "chunk_index": 1,
        "content": "React is a JavaScript frontend library."
    }
]


results = generate_embeddings(sample_chunks)

print("Total chunks:", len(results))

for item in results:
    print("\nChunk ID:", item["chunk_id"])
    print("Content:", item["content"])
    print("Embedding dimensions:", len(item["embedding"]))
    