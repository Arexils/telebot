import requests
from aiogram import types

from loader import dp


@dp.message_handler(commands=['meow'])
async def photo_meow(msg: types.Message):
    response = requests.get('https://aws.random.cat/meow').json().get('file')
    await msg.answer_photo(response)


@dp.message_handler(commands=['dice'], )
async def dice(msg: types.Message):
    """Полный список emoji: 🎲, 🎯, 🏀, ⚽, 🎳, 🎰 """

    await msg.answer_dice('🎲')
