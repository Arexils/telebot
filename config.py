import os

from dotenv import load_dotenv

load_dotenv()

ADMINS = (381762408,)  # Тут ваш id
TOKEN = os.getenv('TOKEN')

BASE_URL = f'https://api.telegram.org/bot{TOKEN}'

if not TOKEN:
    exit('Error: no token provided')
