from aiogram.types import Message

from handlers.flowbutton.shop.filters.filters import IsUser
from handlers.flowbutton.shop.user.menu import delivery_status
from loader import db, dp


@dp.message_handler(IsUser(), text=delivery_status)
async def process_delivery_status(msg: Message):
    with db as conn:
        orders = conn.fetchall(
            'SELECT * FROM orders WHERE cid=?',
            (msg.chat.id,)
        )

    if len(orders) == 0:
        await msg.answer('У вас нет активных заказов.')
    else:
        await delivery_status_answer(msg, orders)


async def delivery_status_answer(message, orders):
    res = ''

    for order in orders:
        res += f'Заказ <b>№{order[3]}</b>'
        answer = [
            ' лежит на складе.',
            ' уже в пути!',
            ' прибыл и ждет вас на почте!'
        ]

        res += f'{answer[0]}\n\n'

    await message.answer(res)
