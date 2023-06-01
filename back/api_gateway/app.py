from flask import Flask
from settings import config
from user_bp import user_blueprint
from doc_bp import document_blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(document_blueprint)
    return app
