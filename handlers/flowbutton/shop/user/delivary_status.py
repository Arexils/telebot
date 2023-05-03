from aiogram.types import CallbackQuery

from handlers.flowbutton.shop.filters.filters import IsUser
from handlers.flowbutton.shop.user.menu import delivery_status
from loader import db, dp


@dp.callback_query_handler(IsUser(), text=delivery_status.callback_data)
async def process_delivery_status(callback: CallbackQuery):
    with db as conn:
        orders = conn.fetchall(
            'SELECT * FROM orders WHERE cid=?',
            (callback.message.chat.id,)
        )

    if len(orders) == 0:
        await callback.answer('У вас нет активных заказов.')
        await callback.message.answer('У вас нет активных заказов.')
    else:
        await delivery_status_answer(callback, orders)


async def delivery_status_answer(callback, orders):
    res = ''

    for order in orders:
        res += f'Заказ <b>№{order[3]}</b>'
        answer = [
            ' лежит на складе.',
            ' уже в пути!',
            ' прибыл и ждет вас на почте!'
        ]

        res += f'{answer[0]}\n\n'

    await callback.message.answer(res)
