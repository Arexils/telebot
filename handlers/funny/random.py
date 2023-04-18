from random import randint

from aiogram import types

from loader import dp
from utils.keyborads.dev_inline import keyboard


@dp.message_handler(commands='random')
async def cmd_random(message: types.Message):
    await message.answer('Нажмите на кнопку, чтобы бот отправил число от 1 до 10', reply_markup=keyboard)


@dp.callback_query_handler(text='random_value')
async def send_random_value(callback: types.CallbackQuery):
    rand = str(randint(1, 10))
    await callback.answer(rand)  # <-- Ответ на callback
    await callback.message.answer(rand)
