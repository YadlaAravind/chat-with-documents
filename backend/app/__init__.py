
from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.extensions import db, migrate, jwt

from app.models.chat import ChatHistory

from app.routes.health import health_bp
from app.routes.documents import documents_bp
from app.routes.search import search_bp
from app.routes.history import history_bp


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    app.config["UPLOAD_FOLDER"].mkdir(
        parents=True,
        exist_ok=True
    )

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": ["http://localhost:5173"]
            }
        }
    )

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Create database tables
    with app.app_context():
        db.create_all()

    # Register routes
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(documents_bp, url_prefix="/api")
    app.register_blueprint(search_bp, url_prefix="/api")
    app.register_blueprint(history_bp, url_prefix="/api")

    return app
