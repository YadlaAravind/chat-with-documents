
from flask import Blueprint, request, jsonify, current_app

from app.services.embedding_service import generate_query_embedding
from app.services.vector_store import search_similar_chunks

from app.extensions import db
from app.models.chat import ChatHistory


search_bp = Blueprint("search", __name__)


def create_fallback_answer(query, results):

    query_lower = query.lower()

    combined_text = "\n".join(
        item["content"] for item in results
    )

    lines = [
        line.strip()
        for line in combined_text.splitlines()
        if line.strip()
    ]

    unique_lines = list(dict.fromkeys(lines))

    # 1. EDUCATION QUESTIONS
    if any(word in query_lower for word in [
        "education", "degree", "college",
        "qualification", "graduation", "study"
    ]):

        keywords = [
            "b.tech",
            "computer science",
            "andhra loyola",
            "2022",
            "2026",
            "75%"
        ]

        answer_lines = [
            line for line in unique_lines
            if any(keyword in line.lower() for keyword in keywords)
        ]

        if answer_lines:
            return (
                "EDUCATION DETAILS\n\n"
                + "\n".join(f"- {line}" for line in answer_lines)
            )

    # 2. TECHNICAL SKILLS QUESTIONS
    if any(word in query_lower for word in [
        "skill", "skills", "technical"
    ]):

        categories = [
            "Programming:",
            "AI & Machine Learning:",
            "Computer Vision:",
            "AI & Deep Learning Libraries:",
            "Hardware & Operating Systems:",
            "Frontend:",
            "Backend:",
            "Databases:",
            "Tools:",
            "Core Skills:"
        ]

        answer_lines = []

        for category in categories:
            for line in unique_lines:
                if line.lower().startswith(category.lower()):
                    answer_lines.append(f"- {line}")
                    break

        if answer_lines:
            return (
                "TECHNICAL SKILLS\n\n"
                + "\n".join(answer_lines)
            )

    # 3. INTERNSHIP QUESTIONS
    if any(word in query_lower for word in [
        "internship", "intern", "intern experience"
    ]):

        keywords = [
            "intern",
            "intern stump",
            "dec 2025",
            "machine learning",
            "model development",
            "model evaluation",
            "preprocessing"
        ]

        answer_lines = [
            line for line in unique_lines
            if any(keyword in line.lower() for keyword in keywords)
        ]

        if answer_lines:
            return (
                "INTERNSHIP EXPERIENCE\n\n"
                + "\n".join(f"- {line}" for line in answer_lines)
            )

    # 4. PROJECT QUESTIONS
    if any(word in query_lower for word in [
        "project", "projects", "application"
    ]):

        answer_lines = [
            line for line in unique_lines
            if any(word in line.lower() for word in [
                "project",
                "developed",
                "built",
                "application",
                "using flask",
                "react"
            ])
        ]

        if answer_lines:
            return (
                "PROJECT INFORMATION\n\n"
                + "\n".join(answer_lines[:12])
            )

    # 5. GENERAL FALLBACK
    relevant_lines = unique_lines[:15]

    return (
        "Relevant information from your document:\n\n"
        + "\n".join(f"- {line}" for line in relevant_lines)
    )


@search_bp.route("/documents/search", methods=["POST"])
def search_documents():

    data = request.get_json(silent=True) or {}

    query = data.get("query", "")
    document_id = data.get("document_id")

    # 1. Validate query
    if not isinstance(query, str) or not query.strip():
        return jsonify({
            "error": "Query is required"
        }), 400

    query = query.strip()

    if len(query) > 2000:
        return jsonify({
            "error": "Query must not exceed 2000 characters"
        }), 400

    # 2. Validate document ID
    if not isinstance(document_id, str) or not document_id.strip():
        return jsonify({
            "error": "Document ID is required"
        }), 400

    document_id = document_id.strip()

    try:

        # 3. Generate query embedding
        query_embedding = generate_query_embedding(query)

        # 4. Retrieve relevant chunks
        results = search_similar_chunks(
            query_embedding,
            document_id=document_id,
            top_k=10
        )

        print("RETRIEVED CHUNKS:", len(results))

        # 5. Handle empty results
        if not results:

            return jsonify({
                "status": "success",
                "query": query,
                "answer": "No relevant document content found.",
                "answer_source": "none",
                "sources": []
            }), 200

        # 6. Generate fast fallback answer
        answer = create_fallback_answer(
            query,
            results
        )

        answer_source = "document_fallback"

        # 7. Save chat history
        chat = ChatHistory(
            document_id=document_id,
            question=query,
            answer=answer
        )

        db.session.add(chat)
        db.session.commit()

        # 8. Prepare source information
        sources = [
            {
                "page_number": item["metadata"]["page_number"],
                "chunk_index": item["metadata"]["chunk_index"],
                "distance": item["distance"]
            }
            for item in results
        ]

        print("SEARCH COMPLETED SUCCESSFULLY")

        # 9. Return response
        return jsonify({
            "status": "success",
            "query": query,
            "answer": answer,
            "answer_source": answer_source,
            "sources": sources
        }), 200

    except Exception:

        db.session.rollback()

        current_app.logger.exception(
            "Document search failed"
        )

        return jsonify({
            "error": "Document search failed"
        }), 500
