from aiogram import types

from loader import dp
from utils.keyborads.dev import kb


@dp.message_handler(commands=['dev', ])
async def command_start(msg: types.Message):
    await msg.answer('кнопкиииии', reply_markup=kb)
