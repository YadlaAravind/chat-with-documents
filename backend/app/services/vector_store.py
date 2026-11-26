
import chromadb
from pathlib import Path

# Persistent ChromaDB storage
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CHROMA_PATH = BASE_DIR / "chroma_db"

client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)


def get_collection():
    collection = client.get_or_create_collection(
        name="documents",
        metadata={"hnsw:space": "cosine"}
    )
    return collection


def store_embeddings(document_id, embedded_chunks):

    if not embedded_chunks:
        return 0

    collection = get_collection()

    print("DOCUMENT ID:", document_id)
    print("EMBEDDED CHUNKS COUNT:", len(embedded_chunks))

    collection.add(
        ids=[
            f"{document_id}_{chunk['chunk_id']}"
            for chunk in embedded_chunks
        ],
        embeddings=[
            chunk["embedding"]
            for chunk in embedded_chunks
        ],
        documents=[
            chunk["content"]
            for chunk in embedded_chunks
        ],
        metadatas=[
            {
                "document_id": document_id,
                "page_number": chunk["page_number"],
                "chunk_index": chunk["chunk_index"]
            }
            for chunk in embedded_chunks
        ]
    )

    print("CHROMA COUNT:", collection.count())

    return len(embedded_chunks)


def search_similar_chunks(query_embedding, document_id=None, top_k=5):

    collection = get_collection()

    if collection.count() == 0:
        return []

    where_filter = None

    if document_id:
        where_filter = {
            "document_id": document_id
        }

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count()),
        where=where_filter,
        include=["documents", "metadatas", "distances"]
    )

    matches = []

    if results["ids"] and results["ids"][0]:
        for i in range(len(results["ids"][0])):
            matches.append({
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            })

    return matches
