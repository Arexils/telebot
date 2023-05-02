from aiogram.types import Message, CallbackQuery, ChatActions

from handlers.flowbutton.shop.filters.filters import IsUser
from handlers.flowbutton.shop.keyboards.inline.categories import categories_markup, category_cb
from handlers.flowbutton.shop.keyboards.inline.products_from_cart import product_markup
from handlers.flowbutton.shop.keyboards.inline.products_from_catalog import product_cb
from handlers.flowbutton.shop.user.menu import catalog
from loader import db, dp


@dp.message_handler(IsUser(), text=catalog)
async def process_catalog(msg: Message):
    await msg.answer(
        'Выберите раздел, чтобы вывести список товаров:',
        reply_markup=categories_markup()
    )


@dp.callback_query_handler(IsUser(), category_cb.filter(action='view'))
async def category_callback_handler(callback: CallbackQuery, callback_data: dict):
    with db as conn:
        products = conn.fetchall(
            """
            SELECT * FROM products product
            WHERE product.tag = (SELECT title FROM categories WHERE idx=?)
            AND product.idx NOT IN (SELECT idx FROM cart WHERE cid = ?)
            """,
            (
                callback_data['id'],
                callback.message.chat.id
            )
        )

    await callback.answer('Все доступные товары.')
    await show_products(callback.message, products)


@dp.callback_query_handler(IsUser(), product_cb.filter(action='add'))
async def add_product_callback_handler(callback: CallbackQuery, callback_data: dict):
    with db as conn:
        conn.query(
            'INSERT INTO cart VALUES (?, ?, 1)',
            (
                callback.message.chat.id,
                callback_data['id']
            )
        )

    await callback.answer('Товар добавлен в корзину!')
    await callback.message.delete()


async def show_products(msg: Message, products):
    if len(products) == 0:
        await msg.answer('Здесь ничего нет 😢')

    else:
        await msg.answer_chat_action(ChatActions.TYPING)
        for idx, title, body, image, price, _ in products:
            markup = product_markup(idx, price)
            text = f'<b>{title}</b>\n\n{body}'

            await msg.answer_photo(
                photo=image,
                caption=text,
                reply_markup=markup
            )
