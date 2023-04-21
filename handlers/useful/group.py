from aiogram import types
from aiogram.dispatcher.filters import AdminFilter, IDFilter

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
