"""
 который получает сообщения, проверяет новое ли оно и если новое,
 а также если это написал пользователь-администратор и текст равен /start,
 он будет отсылать нам обратно сообщение с Привет username
"""
import time

import requests

from config import TOKEN

BASE_URL = f'https://api.telegram.org/bot{TOKEN}'
ADMIN = [381762408, ]  # Тут ваш id


def polling():
    count_msg = 0
    while True:
        time.sleep(1)
        response = requests.get(f'{BASE_URL}/getUpdates').json()
        if count_msg != len(response['result']):
            count_msg = len(response['result'])
            print(count_msg)

            msg = response['result'][-1]['message']
            user_id = msg['from']['id']
            chat_id = msg['chat']['id']

            if user_id in ADMIN:
                print('--- сработало ---')
                headers = {'content-type': 'multipart/form-data'}
                file_id = msg['sticker']['file_id']
                params = {
                    'chat_id': chat_id,
                    'sticker': file_id,
                }
                requests.post(f'{BASE_URL}/sendSticker', params=params, headers=headers)


polling()
