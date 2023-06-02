import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt
import requests
from settings import config
from datetime import timedelta
user_blueprint = Blueprint('users', __name__, url_prefix='/user')
from app import jwt

blacklist = set()
user_api = config["USERS_API"]

@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f"{user_api}/user/login", json=data, headers=headers)
    if response.status_code == 200:
        access_token = create_access_token(identity=response.json()['email'], expires_delta=timedelta(hours=24))
        return jsonify(access_token=access_token), response.status_code
    return jsonify(response.json()), response.status_code


@user_blueprint.route('/registerUser', methods=['POST'])
def create_user():
    data = request.get_json()
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f"{user_api}/user/registerUser", json=data, headers=headers)
    return jsonify(response.json()), response.status_code

@user_blueprint.route('/getUsers', methods=['GET'])
@jwt_required()
def get_usuarios():
    response = requests.get(f"{user_api}/user/getUsers")
    return jsonify(response.json()), response.status_code

@user_blueprint.route('/getUser', methods=['GET'])
@jwt_required()
def get_usuario():
    response = requests.get(f"{user_api}/user/getUser")
    return jsonify(response.json()), response.status_code

@user_blueprint.route('/updateUser', methods=['PUT'])
@jwt_required()
def update_usuario():
    data = request.get_json()
    headers = {'Content-Type': 'application/json'}
    response = requests.put(f"{user_api}/user/updateUser", json=data, headers=headers)
    return jsonify(response.json()), response.status_code

@user_blueprint.route('/delUser', methods=['DELETE'])
@jwt_required()
def delete_usuario():
    data = request.get_json()
    headers = {'Content-Type': 'application/json'}
    response = requests.delete(f"{user_api}/user/delUser", json=data, headers=headers)
    return jsonify(response.json()), response.status_code

@user_blueprint.route('/logout', methods=['POST'])
@jwt_required
def logout():
    jti = get_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Logged out successfully"}), 200

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_data):
    jti = jwt_data['jti']
    return jti in blacklist