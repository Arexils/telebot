from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp


@dp.message_handler(commands=['dev', ])
async def command_dev(msg: types.Message):
    await msg.answer(
        'кнопкиииии',
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                'Первая кнопка!',
                callback_data='button1'
            )
        )
    )
