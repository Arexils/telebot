import os

from aiogram.types import BotCommand
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
    BotCommand('start', 'Стартуем!'),
    BotCommand('info', 'Информационная карточка профиля'),
    BotCommand('poll', 'Запустить голосование'),

    BotCommand('meow', 'Случайное фото котиков'),
    BotCommand('dice', 'Бросить кости'),
    BotCommand('random', 'Кнопка с радомом от 1 до 10'),

    BotCommand('fetchone', 'Получение одной записи БД'),
    BotCommand('fetchall', 'Получение всех ваших записей БД'),
    BotCommand('info_2', 'Информационная карточка профиля'),

    BotCommand('ban', 'Забанить'),
    BotCommand('block_me', 'Забанить'),
    BotCommand('unblock', 'Забанить'),

    BotCommand('menu', 'Команда с кнопками текстовыми'),
    BotCommand('numbers', 'Почти корзина'),
    BotCommand('kb_inline', 'Пример inline кнопки'),
    BotCommand('kb_inline_full', 'Пример inline кнопок'),
    BotCommand('rm', 'Удалить клавиатуру текстовую'),
    BotCommand('multi_lvl_kb', 'Многоуровневая'),
]
