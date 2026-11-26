from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)

@health_bp.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "success",
        "message": "AI Chat with Documents API is running"
    }), 200