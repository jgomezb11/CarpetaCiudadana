import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, Usuario, Carpeta, usuario_schema, usuarios_schema
from apis import DocumentosAPI, APIGovCarpeta

api_gov = APIGovCarpeta()
doc_api = DocumentosAPI()
user_blueprint = Blueprint('users', __name__, url_prefix='/user')

@user_blueprint.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    user = Usuario.query.filter_by(email=email).first()
    if user is None or not check_password_hash(user.password, password):
        return jsonify({"msg": "Bad email or password"}), 401
    return jsonify({"email": email}), 200

@user_blueprint.route('/registerUser', methods=['POST'])
def create_user():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    data = request.get_json()
    id = data.get('id', None)
    name = data.get('name', None)
    address = data.get('address', None)
    email = data.get('email', None)
    phone_number = data.get('phone_number', None)
    password = data.get('password', None)
    if not email or not password or not name or not address or not id:
        return jsonify({"msg": "Missing parameters"}), 400
    if Usuario.query.filter_by(id=id).first() is not None:
        return jsonify({"msg": "User already exists"}), 400
    if api_gov.validateCitizen({"id": id}) == 200:
        return jsonify({"msg": "User already registered in another operator."}), 400
    new_usuario = Usuario(id=id, name=name, address=address, email=email, phone_number=phone_number, password=generate_password_hash(password))
    new_carpeta = Carpeta(id=id, number_of_documents=0, number_non_signed=0, user_id=id)
    new_usuario.carpeta = new_carpeta
    #api_gov.registerCitizen(id, name, address, email)
    db.session.add(new_usuario)
    db.session.commit()
    if doc_api.initial_doc(email) != 201:
        return jsonify({"msg": "There was an error uploading the document"}), 400
    return usuario_schema.jsonify(new_usuario), 201

@user_blueprint.route('/getUsers', methods=['GET'])
def get_usuarios():
    all_usuarios = Usuario.query.all()
    result = usuarios_schema.dump(all_usuarios)
    return jsonify(result)

@user_blueprint.route('/getUser', methods=['GET'])
def get_usuario():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    data = request.get_json()
    id = data.get('id', None)
    if id is None:
        return jsonify({"msg": "No ID specified"}), 400
    usuario = Usuario.query.get(id)
    if usuario is None:
        return jsonify({"msg": "User not found"}), 404
    return usuario_schema.jsonify(usuario)

@user_blueprint.route('/updateUser', methods=['PUT'])
def update_usuario():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    data = request.get_json()
    id = data.get('id', None)
    if id is None:
        return jsonify({"msg": "No ID specified"}), 400
    usuario = Usuario.query.get(id)
    if usuario is None:
        return jsonify({"msg": "User not found"}), 404
    name = data.get('name', None)
    address = data.get('address', None)
    phone_number = data.get('phone_number', None)
    password = data.get('password', None)
    if Usuario.query.filter_by(id=id).first() is not None:
        usuario.name = name if name is not None else usuario.name
        usuario.address = address if address is not None else usuario.address
        usuario.phone_number = phone_number if phone_number is not None else usuario.phone_number
        if password is not None:
            usuario.password = generate_password_hash(password)
        db.session.commit()
        usuario = Usuario.query.get(id)
        return usuario_schema.jsonify(usuario)
    return jsonify({'msg': 'There was a problem with the update. Check that the user exists'})

@user_blueprint.route('/delUser', methods=['DELETE'])
def delete_usuario():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    data = request.get_json()
    id = data.get('id', None)
    usuario = Usuario.query.get(id)
    carpeta = Carpeta.query.filter_by(id=id).first()
    if usuario is None:
        return jsonify({"msg": "User not found"}), 404
    db.session.delete(carpeta)
    db.session.delete(usuario)
    db.session.commit()
    return usuario_schema.jsonify(usuario)