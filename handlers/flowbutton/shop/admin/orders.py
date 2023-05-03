from aiogram.types import Message, CallbackQuery

from handlers.flowbutton.shop.user.menu import orders
from handlers.flowbutton.shop.filters.filters import IsAdmin
from loader import dp, db


@dp.callback_query_handler(IsAdmin(), text=orders.callback_data)
async def process_orders(callback: CallbackQuery):
    with db as conn:
        orders = conn.fetchall('SELECT * FROM orders')

    if len(orders) == 0:
        await callback.answer('У вас нет заказов.')
        await callback.message.answer('У вас нет заказов.')
    else:
        await order_answer(callback.message, orders)
    await callback.answer('')


async def order_answer(message, orders):
    res = ''

    for order in orders:
        res += f'Заказ <b>№{order[3]}</b>\n\n'

    await message.answer(res)
