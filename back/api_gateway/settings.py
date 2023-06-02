import os
from dotenv import load_dotenv

load_dotenv()
config = {
    'DOCUMENTS_API': os.getenv('DOCUMENTS_API'),
    'USERS_API': os.getenv('USERS_API'),
    'NOTIFICATOR_API': os.getenv('NOTIFICATOR_API'),
    'REQUESTS_API': os.getenv('REQUESTS_API'),   
}

flask_config = {
    'JWT_SECRET_KEY': os.getenv('JWT_SECRET_KEY')
}
