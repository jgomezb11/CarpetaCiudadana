from requests_toolbelt.multipart.encoder import MultipartEncoder
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
import requests
from settings import config

documents_api = config["DOCUMENTS_API"]
document_blueprint = Blueprint('documents', __name__, url_prefix='/doc')

@document_blueprint.route('/createDoc', methods=['POST'])
def create_documento():
    if 'file' not in request.files:
        return jsonify({"msg": "No file part in the request"}), 400
    file = request.files['file']
    data = request.form
    if file.filename == '':
        return jsonify({"msg": "No file selected"}), 400
    if not file or not file.filename.lower().endswith('.pdf'):
        return jsonify({"msg": "Not a PDF file"}), 400
    email = data.get('email', "")
    sender = data.get('sender', "")
    is_signed = bool(data.get('is_signed', None))
    multipart_data = MultipartEncoder(
        fields={
            'file': (file.filename, file, 'application/pdf'),
            'email': email,
            'sender': sender,
            'is_signed': str(is_signed),
        }
    )
    headers = {
        'Content-Type': multipart_data.content_type
    }
    response = requests.post(
        f"{documents_api}/doc/createDoc",
        data=multipart_data,
        headers=headers
    )
    return jsonify(response.json()), response.status_code

@document_blueprint.route('/getAll', methods=['GET'])
@jwt_required()
def get_documentos():
    data = request.get_json()
    headers = {'Content-Type': 'application/json'}
    response = requests.get(f"{documents_api}/doc/getAll", json=data, headers=headers)
    return jsonify(response.json()), response.status_code

@document_blueprint.route('/getS3Link', methods=['GET'])
@jwt_required()
def get_s3_link():
    data = request.get_json()
    headers = {'Content-Type': 'application/json'}
    response = requests.get(f"{documents_api}/doc/getS3Link", json=data, headers=headers)
    return jsonify(response.json()), response.status_code

@document_blueprint.route('/delDocument', methods=['DELETE'])
@jwt_required()
def delete_documento():
    data = request.get_json()
    headers = {'Content-Type': 'application/json'}
    response = requests.delete(f"{documents_api}/doc/delDocument", json=data, headers=headers)
    return jsonify(response.json()), response.status_code