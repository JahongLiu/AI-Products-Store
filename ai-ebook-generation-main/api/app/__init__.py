from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.ai_book_generation.limiter.limiter import limiter


def create_app():
    app = Flask(__name__)
    limiter.init_app(app)
    from app.routes import main

    app.register_blueprint(main)

    return app
