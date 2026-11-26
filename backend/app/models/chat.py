from datetime import datetime
from app.extensions import db


class ChatHistory(db.Model):

    __tablename__ = "chat_history"

    id = db.Column(db.Integer, primary_key=True)

    document_id = db.Column(
        db.String(100),
        nullable=False
    )

    question = db.Column(
        db.Text,
        nullable=False
    )

    answer = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )