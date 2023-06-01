import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token
import requests
from settings import config
user_blueprint = Blueprint('users', __name__, url_prefix='/user')

user_api = config["USERS_API"]

@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f"{user_api}/user/login", json=data, headers=headers)
    return jsonify(response.json()), response.status_code

@user_blueprint.route('/registerUser', methods=['POST'])
def create_user():
    data = request.get_json()
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f"{user_api}/user/registerUser", json=data, headers=headers)
    return jsonify(response.json()), response.status_code

@user_blueprint.route('/getUsers', methods=['GET'])
def get_usuarios():
    response = requests.get(f"{user_api}/user/getUsers")
    return jsonify(response.json()), response.status_code

@user_blueprint.route('/getUser', methods=['GET'])
def get_usuario():
    response = requests.get(f"{user_api}/user/getUser")
    return jsonify(response.json()), response.status_code

@user_blueprint.route('/updateUser', methods=['PUT'])
def update_usuario():
    data = request.get_json()
    headers = {'Content-Type': 'application/json'}
    response = requests.put(f"{user_api}/user/updateUser", json=data, headers=headers)
    return jsonify(response.json()), response.status_code

@user_blueprint.route('/delUser', methods=['DELETE'])
def delete_usuario():
    data = request.get_json()
    headers = {'Content-Type': 'application/json'}
    response = requests.delete(f"{user_api}/user/delUser", json=data, headers=headers)
    return jsonify(response.json()), response.status_code