from flask import Blueprint, jsonify, request
import requests
from settings import config

solicitud_blueprint = Blueprint('solicitudes', __name__, url_prefix='/req')
req_api = config['REQUESTS_API']

@solicitud_blueprint.route('/createReq', methods=['POST'])
def create_solicitud():
    data = request.get_json()
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f"{req_api}/req/createReq", json=data, headers=headers)
    return jsonify(response.json()), response.status_code

@solicitud_blueprint.route('/delReq', methods=['DELETE'])
def delete_solicitud():
    data = request.get_json()
    headers = {'Content-Type': 'application/json'}
    response = requests.delete(f"{req_api}/req/delReq", json=data, headers=headers)
    return jsonify(response.json()), response.status_code


@solicitud_blueprint.route('/updateReq', methods=['PUT'])
def update_solicitud():
    data = request.get_json()
    headers = {'Content-Type': 'application/json'}
    response = requests.put(f"{req_api}/req/updateReq", json=data, headers=headers)
    return jsonify(response.json()), response.status_code

@solicitud_blueprint.route('/getAll', methods=['GET'])
def get_solicitudes_by_destinatario():
    data = request.get_json()
    headers = {'Content-Type': 'application/json'}
    response = requests.put(f"{req_api}/req/getAll", json=data, headers=headers)
    return jsonify(response.json()), response.status_code