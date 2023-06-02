from flask import Flask
from flask_jwt_extended import JWTManager
from settings import flask_config

app = Flask(__name__)
jwt = JWTManager(app)

def create_app():
    
    app.config.update(flask_config)
    with app.app_context():
        from user_bp import user_blueprint
        from doc_bp import document_blueprint
        app.register_blueprint(user_blueprint)
        app.register_blueprint(document_blueprint)
    return app
