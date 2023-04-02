import os

from dotenv import load_dotenv

load_dotenv()

ADMINS = (381762408,)  # Тут ваш id
TOKEN = os.getenv('TOKEN')
NGROK = os.getenv('NGROK', '')

# настройки webhook
WEBHOOK_PATH = ''
WEBHOOK_URL = f'{NGROK}{WEBHOOK_PATH}'

# настройки веб сервера
WEBAPP_HOST = '127.0.0.1'  # or ip
WEBAPP_PORT = 8000

if not TOKEN:
    exit('Error: no token provided')
