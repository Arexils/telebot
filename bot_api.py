import json

import requests

from config import BASE_URL


def pulling():
    data = dict(
        method='getUpdates',
        offset=0,
        timeout=60,
    )

    while True:
        try:
            req = requests.post(f'{BASE_URL}/', data=data, ).json()
        except ValueError:
            continue
        if not req['ok'] or not req['result']:
            continue
        for r in req['result'][:]:
            if r.get('message', dict()).get('text') is not None:
                data['offset'] = r['update_id'] + 1
                message = r['message']
                chat_id = message['chat']['id']

                keyboard = json.dumps(
                    {
                        'inline_keyboard': [
                            [
                                {'text': 'Да', 'callback_data': '1'},
                                {'text': 'Нет', 'callback_data': '2'},
                            ],
                            [
                                {'text': 'Google', 'url': 'www.google.ru'},
                            ],
                        ]
                    }
                )

                params = {
                    'method': 'sendMessage',
                    'chat_id': chat_id,
                    'text': message['text'],
                    'reply_markup': keyboard,
                }
                requests.post(f'{BASE_URL}/', data=params)


if __name__ == '__main__':
    pulling()
