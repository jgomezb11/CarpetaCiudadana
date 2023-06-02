from flask import Blueprint, jsonify, request
from utils import send_email

notification_blueprint = Blueprint('notifications', __name__, url_prefix='/noti')

@notification_blueprint.route('/notificateUser', methods=['POST'])
def notificate():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    data = request.get_json()
    email = data.get('email', None)
    mensaje = data.get('mensaje', None)
    adjuntos = data.get("adjuntos", None)
    sujeto = data.get("sujeto", None)
    if not email or not mensaje or not sujeto:
        return jsonify({"msg": "Missing parameters"}), 400
    send_email(email, sujeto, mensaje, adjuntos)
    return jsonify({"msg": "Done!"}), 200