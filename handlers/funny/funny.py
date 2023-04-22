import sqlite3

import requests
from aiogram import types
from aiogram.dispatcher import filters
from aiogram.dispatcher.filters import ChatTypeFilter

from loader import dp


@dp.message_handler(commands=['meow'])
async def photo_meow(msg: types.Message):
    response = requests.get('https://api.thecatapi.com/v1/images/search?format=json').json()[0].get('url')
    data = (msg.from_user.id, msg.date.timestamp(), response)
    with sqlite3.connect(database='database.db') as conn:
        cur = conn.cursor()
        cur.execute(
            """
            insert into history_cats(user_id, timestamp, url) values (?,?,?)
        """,
            data
        )
        conn.commit()
    await msg.answer_photo(response)


@dp.message_handler(commands=['dice'], )
async def dice(msg: types.Message):
    """Полный список emoji: 🎲, 🎯, 🏀, ⚽, 🎳, 🎰 """

    await msg.answer_dice('🎲')


@dp.message_handler(ChatTypeFilter(types.ChatType.PRIVATE), commands=['meow_all'], )
async def photo_meow_all(msg: types.Message):
    # if msg.chat.type == 'private':
    with sqlite3.connect(database='database.db') as conn:
        cur = conn.cursor()
        all_cats = cur.execute(
            """
            select url from history_cats;
        """
        ).fetchall()
        for cat in all_cats:
            await msg.answer_photo(cat[0])
