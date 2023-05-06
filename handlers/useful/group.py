from aiogram import types
from aiogram.dispatcher.filters import AdminFilter, IDFilter
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

import config
from loader import dp


@dp.message_handler(AdminFilter() | IDFilter(config.ADMINS), commands=['poll', 'перерыв'], )
async def send_poll_to_user(msg: types.Message):
    poll = {
        'question': 'Время отдыха',
        'options': ['Без перерыва', '5 минут', '10 минут'],
        'is_anonymous': True,
    }

    await msg.answer_poll(**poll)


@dp.message_handler(commands='extension_translate')
async def extension_link(msg: Message):
    await msg.answer(
        'Расширение которое переводит видео ',
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton('Ссылка', url='https://github.com/ilyhalight/voice-over-translation')
        )
    )
