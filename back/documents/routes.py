import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required


document_blueprint = Blueprint('documents', __name__, url_prefix='/doc')

@document_blueprint.route('/<user_id>/documentos', methods=['POST'])
@jwt_required()
def create_documento():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    data = request.get_json()
    from app import Documento, Usuario, Carpeta, documento_schema, db
    if 'file' not in request.files:
        return jsonify({"msg": "No file part in the request"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"msg": "No file selected"}), 400
    if not file or not file.filename.lower().endswith('.pdf'):
        return jsonify({"msg": "Not a PDF file"}), 400
    usuario = Usuario.query.get(data.email)
    if usuario is None:
        return jsonify({"msg": "User not found"}), 404
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    data = request.get_json()
    name = file.filename.lower()
    s3_link = data.get('s3_link', None)
    is_signed = data.get('is_signed', None)
    owner = data.email
    sender = data.get('sender', None)
    # date_of_upload es generado automáticamente
    if not name or not s3_link or not owner or not sender:
        return jsonify({"msg": "Missing parameters"}), 400

    documento = Documento(name=name, s3_link=s3_link, is_signed=is_signed, owner=owner, sender=sender, carpeta_id=usuario.carpeta.id)
    db.session.add(documento)
    db.session.commit()

    return documento_schema.jsonify(documento), 201

@document_blueprint.route('/getAll', methods=['GET'])
@jwt_required()
def get_documentos():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    data = request.get_json()
    from app import Usuario, documentos_schema
    usuario = Usuario.query.get(data.id)
    if usuario is None:
        return jsonify({"msg": "User not found"}), 404
    documentos = usuario.carpeta.documentos
    return documentos_schema.jsonify(documentos)

@document_blueprint.route('/getS3Link', methods=['GET'])
@jwt_required()
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
@jwt_required()
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