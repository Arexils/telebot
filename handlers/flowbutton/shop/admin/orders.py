from aiogram.types import Message

from handlers.flowbutton.shop.user.menu import orders
from handlers.flowbutton.shop.filters.filters import IsAdmin
from loader import dp, db


@dp.message_handler(IsAdmin(), text=orders)
async def process_orders(msg: Message):
    with db as conn:
        orders = conn.fetchall('SELECT * FROM orders')

    if len(orders) == 0:
        await msg.answer('У вас нет заказов.')
    else:
        await order_answer(msg, orders)


async def order_answer(message, orders):
    res = ''

    for order in orders:
        res += f'Заказ <b>№{order[3]}</b>\n\n'

    await message.answer(res)
