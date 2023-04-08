import os

from aiogram import types
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

COMMANDS = [
    types.BotCommand('start', 'Стартуем!'),
    types.BotCommand('meow', 'Случайное фото котиков'),
    types.BotCommand('dice', 'Бросить кости'),
    types.BotCommand('fetchone', 'Получение одной записи БД'),
    types.BotCommand('fetchall', 'Получение всех ваших записей БД'),
    types.BotCommand('info', 'Информационная карточка профиля'),
    types.BotCommand('info_2', 'Информационная карточка профиля'),
    types.BotCommand('poll', 'Запустить голосование'),
    types.BotCommand('ban', 'Забанить'),
]
