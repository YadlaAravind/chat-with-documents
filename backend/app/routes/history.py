
from flask import Blueprint, jsonify, request

from app.models.chat import ChatHistory


history_bp = Blueprint("history", __name__)


@history_bp.route("/documents/history/<document_id>", methods=["GET"])
def get_chat_history(document_id):

    chats = (
        ChatHistory.query
        .filter_by(document_id=document_id)
        .order_by(ChatHistory.created_at.asc())
        .all()
    )

    return jsonify({
        "status": "success",
        "total": len(chats),
        "history": [
            {
                "id": chat.id,
                "question": chat.question,
                "answer": chat.answer,
                "created_at": chat.created_at.isoformat()
            }
            for chat in chats
        ]
    }), 200
