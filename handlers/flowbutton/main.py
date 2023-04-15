from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from loader import dp


@dp.message_handler(commands='rm')
async def remove_kb(msg: types.Message):
    await msg.reply('убрал клавиатуру', reply_markup=ReplyKeyboardRemove())
