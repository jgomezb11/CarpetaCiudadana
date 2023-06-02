from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from settings import flask_config

app = Flask(__name__)
cors = CORS(app)
jwt = JWTManager(app)

def create_app():
    
    app.config.update(flask_config)
    with app.app_context():
        from user_bp import user_blueprint
        from doc_bp import document_blueprint
        from request_bp import solicitud_blueprint
        app.register_blueprint(user_blueprint)
        app.register_blueprint(document_blueprint)
        app.register_blueprint(solicitud_blueprint)
    return app
