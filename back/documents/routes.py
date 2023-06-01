import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from flask import Blueprint, jsonify, request
from utils import s3

s3_handler = s3()

document_blueprint = Blueprint('documents', __name__, url_prefix='/doc')

@document_blueprint.route('/createDoc', methods=['POST'])
def create_documento():
    from app import Documento, Usuario, documento_schema, db
    file = request.files['file']
    data = request.form
    usuario = Usuario.query.filter_by(email=data.get('email', "")).first()
    if usuario is None:
        return jsonify({"msg": "User not found"}), 404
    name = file.filename.lower()
    is_signed = bool(data.get('is_signed', None))
    owner = data.get("email", None)
    sender = data.get('sender', None)
    if not name or not owner or not sender:
        return jsonify({"msg": "Missing parameters"}), 400
    s3_file_name = f"{usuario.email}/{name}"
    s3_link = s3_handler.upload_file(file, s3_file_name)
    documento = Documento(name=name, s3_link=s3_link, is_signed=is_signed, owner=owner, sender=sender, carpeta_id=usuario.carpeta.id)
    db.session.add(documento)
    db.session.commit()

    return documento_schema.jsonify(documento), 201

@document_blueprint.route('/getAll', methods=['GET'])
def get_documentos():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    data = request.get_json()
    from app import Usuario, documentos_schema
    usuario = Usuario.query.get(data.get('id'))
    if usuario is None:
        return jsonify({"msg": "User not found"}), 404
    documentos = usuario.carpeta.documentos
    return documentos_schema.jsonify(documentos)

@document_blueprint.route('/getS3Link', methods=['GET'])
def get_s3_link():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    data = request.get_json()
    from app import Documento
    documento = Documento.query.get(data.name)
    if documento is None:
        return jsonify({"msg": "Document not found"}), 404
    return jsonify({"s3_link": documento.s3_link})

@document_blueprint.route('/delDocument', methods=['DELETE'])
def delete_documento():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    data = request.get_json()
    from app import Documento, db, documento_schema
    documento = Documento.query.get(data.name)
    if documento is None:
        return jsonify({"msg": "Document not found"}), 404
    db.session.delete(documento)
    db.session.commit()
    return documento_schema.jsonify(documento)