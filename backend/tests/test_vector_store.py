
from app.services.embedding_service import generate_embeddings
from app.services.vector_store import store_embeddings, get_collection


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
    }
]

embedded_chunks = generate_embeddings(sample_chunks)

total = store_embeddings(
    "test_document_001",
    embedded_chunks
)

print("Stored chunks:", total)

collection = get_collection()

print("Total records in ChromaDB:", collection.count())
