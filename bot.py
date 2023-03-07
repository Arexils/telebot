"""
Реализовать эхо бота с использование Telegram bot api. Бот должен не только принимать сообщения, но и изображения
"""
import requests

from config import TOKEN

BASE_URL = f'https://api.telegram.org/bot{TOKEN}'
ADMINS = [381762408, ]  # Тут ваш id


def pulling():
    count_message = 0
    while True:
        response = requests.get(f'{BASE_URL}/getUpdates').json()
        if count_message != len(response['result']):
            count_message = len(response['result'])
            try:
                message = response['result'][-1]['message']
                chat_id = message['chat']['id']

                json_keyboard = {
                    'method': 'sendMessage',
                    'chat_id': chat_id,
                    'text': 'Какая-то клавиатура',
                    'reply_markup': {

                        'keyboard': [
                            [
                                {
                                    'text': 'YeaS',
                                },
                                {
                                    'text': 'No!',
                                },
                            ],
                            [
                                'Ряд 2',
                            ],

                        ]
                    },
                    'resize_keyboard': True,
                    'one_time_keyboard': False,
                }
                requests.post(f'{BASE_URL}/', json=json_keyboard)
            except Exception as error:
                print(f'Случилась ошибка: {error}')


pulling()
