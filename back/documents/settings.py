import os
from dotenv import load_dotenv

load_dotenv()
config = {
    'SQLALCHEMY_DATABASE_URI': os.getenv('DATABASE_URI'),
    'API_GATEWAY': os.getenv('API_GATEWAY')
}
