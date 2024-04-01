import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
API_HOST = os.getenv('API_HOST', default='api-service:80')
