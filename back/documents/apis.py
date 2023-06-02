import requests
from settings import config

class API:
    def authenticate_document(self, data):
        endpoint = 'http://169.51.195.62:30174/apis/authenticateDocument/'
        response = requests.get(endpoint)
        return response.status_code
    
    def notificate_user(self, email, sujeto, mensaje, adjuntos=None):
        endpoint = config['API_GATEWAY'] + "/noti/notificateUser"
        data = {
            "mensaje": mensaje,
            "email": email,
            "sujeto": sujeto,
            "adjuntos": adjuntos,
        }
        requests.post(endpoint, json=data)
