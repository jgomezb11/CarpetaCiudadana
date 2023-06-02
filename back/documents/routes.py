from flask import Blueprint, jsonify, request
from utils import s3
import requests
from apis import API

apis = API()

s3_handler = s3()

document_blueprint = Blueprint('documents', __name__, url_prefix='/doc')

@document_blueprint.route('/createDoc', methods=['POST'])
def create_documento():
    from app import Documento, Usuario, Carpeta, documento_schema, db
    file = request.files['file']
    data = request.form
    usuario = Usuario.query.filter_by(email=data.get('email', "")).first()
    if usuario is None:
        return jsonify({"msg": "User not found"}), 400
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
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    data = request.get_json()
    links = data.get('links', [])
    sender = data.get('sender', '')
    owner = data.get('owner', '')
    if not links or not sender or not owner:
        return jsonify({"msg": "Missing required parameters"}), 400
    sujeto = f"Notificacion de recibo de archivos"
    mensaje = f"El usuario {sender} te acaba de mandar este paquete de archivos a traves del Operador123"
    apis.notificate_user(owner, sujeto, mensaje, links)
    return jsonify({"msg": "Notified successfully!"}), 201


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
        return jsonify({"msg": "Missing id in request"}), 400
    documento = Documento.query.get(id)
    if documento is None:
        return jsonify({"msg": "Document not found"}), 404
    return jsonify({"s3_link": documento.s3_link})

@document_blueprint.route('/delDocument', methods=['POST'])
def delete_documento():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    data = request.get_json()
    from app import Documento, db, documento_schema
    id = data.get('id', None)
    if not id:
        return jsonify({"msg": "Missing id in request"}), 400
    documento = Documento.query.get(id)
    if documento is None:
        return jsonify({"msg": "Document not found"}), 401
    s3_handler.delete_file(documento.s3_link)
    db.session.delete(documento)
    db.session.commit()
    return documento_schema.jsonify(documento)