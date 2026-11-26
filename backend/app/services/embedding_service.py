
from sentence_transformers import SentenceTransformer

_model = None


def get_embedding_model():
    global _model

    if _model is None:
        print("Loading embedding model...")

        _model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    return _model


def generate_embeddings(chunks):

    if not chunks:
        return []

    model = get_embedding_model()

    texts = [
        chunk["content"]
        for chunk in chunks
    ]

    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )

    results = []

    for chunk, embedding in zip(chunks, embeddings):

        results.append({
            **chunk,
            "embedding": embedding.tolist()
        })

    print("GENERATED EMBEDDINGS:", len(results))

    return results


def generate_query_embedding(query):

    model = get_embedding_model()

    embedding = model.encode(
        query,
        normalize_embeddings=True
    )

    return embedding.tolist()
