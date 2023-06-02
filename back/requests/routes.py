from app import db, Usuario, Solicitud, solicitud_schema, solicitudes_schema
from flask import Blueprint, jsonify, request

solicitud_blueprint = Blueprint('solicitudes', __name__, url_prefix='/req')

@solicitud_blueprint.route('/createReq', methods=['POST'])
def create_solicitud():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    data = request.get_json()
    remitente=data.get('remitente', '')
    usuario = Usuario.query.filter_by(email=remitente).first()
    if not usuario:
        return jsonify({"msg": "User doesn't exist in this operator"}), 400
    new_solicitud = Solicitud(
        nombres=data.get('nombres', []),
        remitente=remitente,
        destinatario=data.get('destinatario', ''),
        estado="PENDIENTE",
        usuario_id=usuario.id
    )
    db.session.add(new_solicitud)
    db.session.commit()
    return solicitud_schema.jsonify(new_solicitud), 201

@solicitud_blueprint.route('/delReq', methods=['DELETE'])
def delete_solicitud():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    data = request.get_json()
    solicitud = Solicitud.query.get(data.get('id'))
    if solicitud is None:
        return jsonify({"msg": "Solicitud not found"}), 404
    db.session.delete(solicitud)
    db.session.commit()
    return solicitud_schema.jsonify(solicitud)

@solicitud_blueprint.route('/updateReq', methods=['PUT'])
def update_solicitud():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    data = request.get_json()
    solicitud = Solicitud.query.get(data.get('id'))
    if solicitud is None:
        return jsonify({"msg": "Solicitud not found"}), 400
    data = request.get_json()
    if data.get('estado') not in {"PENDIENTE", "APROBADO", "RECHAZADO", None}:
        return jsonify({"msg": "Unexpected state."}), 40
    solicitud.estado = data.get('estado', solicitud.estado)
    db.session.commit()
    return solicitud_schema.jsonify(solicitud)

@solicitud_blueprint.route('/getAll', methods=['GET'])
def get_solicitudes_by_destinatario():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    data = request.get_json()
    solicitudes = Solicitud.query.filter_by(destinatario=data.get('destinatario')).all()
    return solicitudes_schema.jsonify(solicitudes)