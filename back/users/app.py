from flask import Flask
from settings import config
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

app = Flask(__name__)
app.config.update(config)
db = SQLAlchemy(app)
ma = Marshmallow(app)
class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True, unique=True)
    phone_number = db.Column(db.String(20), nullable=True)
    carpeta = db.relationship('Carpeta', backref='usuario', uselist=False)


class Carpeta(db.Model):
    __tablename__ = 'carpeta'
    id = db.Column(db.String(50), primary_key=True)
    number_of_documents = db.Column(db.Integer, nullable=False)
    number_non_signed = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(50), db.ForeignKey('usuario.id'), nullable=False)
    documentos = db.relationship('Documento', backref='carpeta', lazy=True)


class Documento(db.Model):
    __tablename__ = 'documento'
    name = db.Column(db.String(50), primary_key=True)
    s3_link = db.Column(db.String(200), nullable=False)
    is_signed = db.Column(db.Boolean, nullable=False)
    owner = db.Column(db.String(50), nullable=False)
    sender = db.Column(db.String(50), nullable=False)
    date_of_upload = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    carpeta_id = db.Column(db.String(50), db.ForeignKey('carpeta.id'), nullable=False)


class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)

def create_app():
    global app
    with app.app_context():
        from routes import user_blueprint
        app.register_blueprint(user_blueprint)
        db.create_all()
    return app
