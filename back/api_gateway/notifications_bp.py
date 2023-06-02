from flask import Blueprint, jsonify, request
from settings import config
import requests

notification_blueprint = Blueprint('notifications', __name__, url_prefix='/noti')
noti_api = config['NOTIFICATOR_API']

@notification_blueprint.route('/notificateUser', methods=['POST'])
def notificate():
    data = request.get_json()
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f"{noti_api}/noti/notificateUser", json=data, headers=headers)
    return jsonify(response.json()), response.status_code
