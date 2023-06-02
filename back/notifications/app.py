from flask import Flask
from settings import config
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config.update(config)

def create_app():
    global app
    with app.app_context():
        from routes import notification_blueprint
        app.register_blueprint(notification_blueprint)
    return app
