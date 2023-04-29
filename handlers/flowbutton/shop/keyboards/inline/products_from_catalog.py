from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

product_cb = CallbackData('product', 'id', 'action')


def product_markup(idx='', price=0):
    global product_cb

    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            f'Добавить в корзину - {price}₽',
            callback_data=product_cb.new(
                id=idx,
                action='add',
            )
        )
    )
