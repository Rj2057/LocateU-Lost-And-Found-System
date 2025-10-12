import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'LostAndFoundDB')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_CHARSET = os.getenv('DB_CHARSET', 'utf8mb4')
    APP_SECRET_KEY = os.getenv('APP_SECRET_KEY', 'default_secret_key')
    APP_DEBUG = os.getenv('APP_DEBUG', 'True') == 'True'

