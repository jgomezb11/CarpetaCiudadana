from flask import Blueprint, jsonify, request
from utils import s3
import requests

s3_handler = s3()

document_blueprint = Blueprint('documents', __name__, url_prefix='/doc')

@document_blueprint.route('/createDoc', methods=['POST'])
def create_documento():
    from app import Documento, Usuario, Carpeta, documento_schema, db
    file = request.files['file']
    data = request.form
    usuario = Usuario.query.filter_by(email=data.get('email', "")).first()
    if usuario is None:
        return jsonify({"msg": "User not found"}), 404
    name = file.filename.lower()
    is_signed = bool(data.get('is_signed', False))
    owner = data.get("email", None)
    sender = data.get('sender', None)
    if not name or not owner or not sender:
        return jsonify({"msg": "Missing parameters"}), 400
    s3_file_name = f"{usuario.email}/{name}"
    s3_link = s3_handler.upload_file(file, s3_file_name)
    carpeta = Carpeta.query.get(usuario.id)
    carpeta.number_of_documents = carpeta.number_of_documents + 1
    if not is_signed:
        carpeta.number_non_signed = carpeta.number_non_signed + 1
    documento = Documento(name=name, s3_link=s3_link, is_signed=is_signed, owner=owner, sender=sender, carpeta_id=usuario.carpeta.id)
    db.session.add(documento)
    db.session.commit()
    return documento_schema.jsonify(documento), 201


@document_blueprint.route('/recvDocs', methods=['POST'])
def recv_docs():
    from app import Documento, Usuario, db
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    data = request.get_json()
    links = data.get('links', [])
    sender = data.get('sender', '')
    owner = data.get('owner', '')
    usuario = Usuario.query.filter_by(email=owner).first()
    if not usuario:
        return jsonify({"msg": "User not found"}), 404
    if not links or not sender or not owner:
        return jsonify({"msg": "Missing required parameters"}), 400
    for link in links:
        response = requests.get(link)
        file_content = response.content
        file_name = f"{owner}/{link.split('/')[-1]}"
        s3_handler.upload_file(file_content, file_name)
        documento = Documento(
            name="Documento",
            s3_link=link,
            is_signed=True,
            owner=owner,
            sender=sender,
            carpeta_id=usuario.carpeta_id
        )
        db.session.add(documento)
    db.session.commit()
    return jsonify({"msg": "Documents created successfully"}), 201


@document_blueprint.route('/sendDocs', methods=['POST'])
def send_docs():
    from app import Documento
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    data = request.get_json()
    names = data.get('names', [])
    sender = data.get('sender', '')
    owner = data.get('owner', '')
    url_operador = data.get('url_operador', '')
    if not names or not sender or not owner or not url_operador:
        return jsonify({"msg": "Missing required parameters"}), 400
    s3_links = []
    for name in names:
        documento = Documento.query.filter_by(name=name, email=sender).first()
        if documento:
            s3_links.append(documento.s3_link)
    headers = {'Content-Type': 'application/json'}
    request_data = {
        "sender": sender,
        "s3_links": s3_links
    }
    requests.post(url_operador, json=request_data, headers=headers)
    return jsonify(request_data), 200


@document_blueprint.route('/getAll', methods=['POST'])
def get_documentos():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    data = request.get_json()
    from app import Usuario, documentos_schema
    email = data.get('email', None)
    if not email:
        return jsonify({"msg": "Missing email in request"}), 400
    usuario = Usuario.query.filter_by(email=email).first()
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
    id = data.get('id', None)
    if not id:
        return jsonify({"msg": "Missing name in request"}), 400
    documento = Documento.query.get(id)
    if documento is None:
        return jsonify({"msg": "Document not found"}), 404
    return jsonify({"s3_link": documento.s3_link})

@document_blueprint.route('/delDocument', methods=['DELETE'])
def delete_documento():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    data = request.get_json()
    from app import Documento, db, documento_schema
    id = data.get('id', None)
    if not id:
        return jsonify({"msg": "Missing name in request"}), 400
    documento = Documento.query.get(id)
    if documento is None:
        return jsonify({"msg": "Document not found"}), 401
    if documento.is_signed:
        return jsonify({"msg": "You can't delete signed documents"}), 401
    s3_handler.delete_file(documento.s3_link)
    db.session.delete(documento)
    db.session.commit()
    return documento_schema.jsonify(documento)