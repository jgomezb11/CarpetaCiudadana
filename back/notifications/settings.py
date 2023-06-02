import os
from dotenv import load_dotenv

load_dotenv()
config = {
    'EMAIL': os.getenv('EMAIL'),
    'PASS': os.getenv('PASS')
}
