import requests
# Funciones para comunicarse con el end-point del gobierno

class API:
    def authenticate_document(self, data):
        endpoint = 'http://169.51.195.62:30174/apis/authenticateDocument/'
        response = requests.get(endpoint)
        return response.status_code