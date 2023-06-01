from dotenv import load_dotenv
import os
import requests
# Funciones para comunicarse con el end-point del gobierno

load_dotenv()

class API:
    def registerCitizen(self, id, name, address, email):
        url = "http://169.51.195.62:30174/apis/registerCitizen"
        data = {
            "id": id,
            "name": name,
            "address": address,
            "email": email,
            "operatorId": os.getenv("OPERATOR_ID"),
            "operatorName": os.getenv("OPERATOR_NAME")
        }
        response = requests.post(url, json=data)
        return response.status_code == 201


    def validateCitizen(self, data):
        id_citizen = data.get('id')
        endpoint = f'http://169.51.195.62:30174/apis/validateCitizen/{id_citizen}'
        response = requests.get(endpoint)
        return response.status_code
