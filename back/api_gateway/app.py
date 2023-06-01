from flask import Flask
from user_bp import user_blueprint
from doc_bp import document_blueprint
from flask_jwt_extended import JWTManager
from settings import flask_config

def create_app():
    app = Flask(__name__)
    app.config.update(flask_config)
    jwt = JWTManager(app)   
    app.register_blueprint(user_blueprint)
    app.register_blueprint(document_blueprint)
    return app
