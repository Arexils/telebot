import logging

import requests
from aiogram.types import Message, CallbackQuery

from config import ADMINS, KINOPOISK
from handlers.films.keyborads import main_menu, randon_film_kb, btn_reviews
from loader import dp

headers = {'accept': 'application/json', 'X-API-KEY': KINOPOISK}  # указать свой токен
url = 'https://api.kinopoisk.dev/'


@dp.message_handler(commands=['films'])
async def get_menu(msg: Message):
    if msg.chat.id in ADMINS:
        await msg.answer('Нажмите на кнопку для получения фильма', reply_markup=main_menu)


@dp.callback_query_handler(text='random')
async def get_random(callback: CallbackQuery):
    resp = requests.get(url + 'v1/movie/random', headers=headers).json()
    title = resp['name']
    description = resp['description']
    year = resp['year']
    rating = resp['rating']['kp']
    poster = resp['poster']['url']
    str_film = ''
    try:
        url_film = resp['videos']['trailers'][0]['url']
        str_film = f'<b>Трейлер:</b> {url_film}\n\n'

    except (IndexError, KeyError):
        logging.info('Нет трейлера')

    await callback.answer(callback.id)
    await callback.message.answer_photo(
        photo=poster,
        caption=(
            f'<b>Фильм:</b> {title}\n\n'
            f'<b>Описание:</b> {description}\n\n'
            f'<b>Год выхода:</b> {year}\n\n'
            f'<b>Рейтинг:</b> {rating}\n\n'
            f'{str_film}'
            f'\n\n'
        ),
        reply_markup=randon_film_kb
    )


@dp.callback_query_handler(text=btn_reviews.callback_data)
async def get_reviews(callback: CallbackQuery):
    resp = requests.get(url + 'v1/review?page=1&limit=3', headers=headers).json()

    resp = resp['docs']
    for rw in resp:
        id_ = rw['movieId']
        r_film = requests.get(url + f'v1.3/movie/{id_}', headers=headers).json()
        title_film = r_film.get('name', '')
        title = rw['title']
        review = rw['review']
        author = rw['author']
        await callback.answer(callback.id)

        await callback.message.answer(
            (
                f'Фильм: {title_film}\n'
                f'Заголовок: {title}\n'
                f'Обзор: {review}\n'
                f'Автор: {author}\n'
                f'________________\n'
            )
        )
