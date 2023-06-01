import os
from dotenv import load_dotenv

load_dotenv()
config = {
    'JWT_SECRET_KEY': os.getenv('JWT_SECRET_KEY'),
    'SQLALCHEMY_DATABASE_URI': os.getenv('DATABASE_URI')
}
