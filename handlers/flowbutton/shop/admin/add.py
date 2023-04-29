from hashlib import md5

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ContentType, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.types.chat import ChatActions
from aiogram.utils.callback_data import CallbackData

from handlers.flowbutton.shop.filters.filters import IsAdmin
from handlers.flowbutton.shop.keyboards.default.markups import cancel_message, back_message, back_markup, check_markup, all_right_message
from handlers.flowbutton.shop.shop import CategoryState, ProductState
from handlers.flowbutton.shop.user.menu import settings
from loader import dp, db, bot

category_cb = CallbackData('category', 'id', 'action')
product_cb = CallbackData('product', 'id', 'action')

add_product = InlineKeyboardButton('➕ Добавить товар', callback_data='add_product')
delete_category = InlineKeyboardButton('🗑️ Удалить категорию', callback_data='delete_category')


@dp.callback_query_handler(IsAdmin(), text=settings.callback_data)
async def process_settings(callback: CallbackQuery | Message):
    markup = InlineKeyboardMarkup()

    with db as conn:
        for idx, title in conn.fetchall('SELECT * FROM categories'):
            markup.add(InlineKeyboardButton(
                title, callback_data=category_cb.new(id=idx, action='view')))

    markup.add(
        InlineKeyboardButton(
            '+ Добавить категорию',
            callback_data='add_category',
        )
    )
    try:
        await callback.message.edit_text('Настройка категорий:', reply_markup=markup)
        await callback.answer('+ Добавить категорию')
    except AttributeError:
        await callback.answer('Настройка категорий:', reply_markup=markup)


@dp.callback_query_handler(IsAdmin(), category_cb.filter(action='view'))
async def category_callback_handler(callback: CallbackQuery, callback_data: dict, state: FSMContext):
    category_idx = callback_data.get('id')
    with db as conn:
        products = conn.fetchall(
            """
                SELECT * FROM products product
                WHERE product.tag = (SELECT title FROM categories WHERE idx=?)
            """,
            (category_idx,)
        )

    await callback.message.delete()
    await callback.answer('Все добавленные товары в эту категорию.')
    await state.update_data(category_index=category_idx)
    await show_products(callback.message, products, category_idx)


# category
@dp.callback_query_handler(IsAdmin(), text='add_category')
async def add_category_callback_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('Название категории?')
    await state.set_state(CategoryState.title.state)


@dp.message_handler(IsAdmin(), state=CategoryState.title)
async def set_category_title_handler(message: Message, state: FSMContext):
    category = message.text
    idx = md5(category.encode('utf-8')).hexdigest()
    with db as conn:
        conn.query('INSERT INTO categories VALUES (?, ?)', (idx, category))

    await state.finish()
    await process_settings(message)


@dp.callback_query_handler(IsAdmin(), text=delete_category.callback_data)
async def delete_category_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    with db as conn:
        if 'category_index' in data:
            idx = data['category_index']
            conn.query(
                'DELETE FROM products WHERE tag IN (SELECT title FROM categories WHERE idx=?)',
                (idx,)
            )
            conn.query(
                'DELETE FROM categories WHERE idx=?',
                (idx,)
            )

            await process_settings(callback)
            await callback.answer('Готово!')


# add product
@dp.callback_query_handler(IsAdmin(), text=add_product.callback_data)
async def process_add_product(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ProductState.title.state)
    await callback.message.answer('Название?', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(cancel_message))
    await callback.answer('Название?')


@dp.message_handler(IsAdmin(), text=cancel_message, state=ProductState.title)
async def process_cancel(message: Message, state: FSMContext):
    await message.answer('Ок, отменено!', reply_markup=ReplyKeyboardRemove())
    await state.finish()

    await process_settings(message)


@dp.message_handler(IsAdmin(), text=back_message, state=ProductState.title)
async def process_title_back(message: Message, state: FSMContext):
    await process_add_product(message)


@dp.message_handler(IsAdmin(), state=ProductState.title)
async def process_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(ProductState.body.state)
    await message.answer('Описание?', reply_markup=back_markup())


@dp.message_handler(IsAdmin(), text=back_message, state=ProductState.body)
async def process_body_back(message: Message, state: FSMContext):
    await state.set_state(ProductState.title.state)
    data = await state.get_data()
    title = data.get('title')
    await message.answer(f"Изменить название с <b>{title}</b>?", reply_markup=back_markup())


@dp.message_handler(IsAdmin(), state=ProductState.body)
async def process_body(message: Message, state: FSMContext):
    await state.update_data(body=message.text)
    await state.set_state(ProductState.image.state)
    await message.answer('Фото?', reply_markup=back_markup())


@dp.message_handler(IsAdmin(), content_types=ContentType.PHOTO, state=ProductState.image)
async def process_image_photo(message: Message, state: FSMContext):
    await state.update_data(image=message.photo[-1].file_id)
    await state.set_state(ProductState.price.state)
    await message.answer('Цена?', reply_markup=back_markup())


@dp.message_handler(IsAdmin(), content_types=ContentType.TEXT, state=ProductState.image)
async def process_image_url(message: Message, state: FSMContext):
    if message.text == back_message:
        await state.set_state(ProductState.body.state)
        data = await state.get_data()
        body = data.get('body')
        await message.answer(f"Изменить описание с <b>{body}</b>?", reply_markup=back_markup())

    else:
        await message.answer('Вам нужно прислать фото товара.')


@dp.message_handler(IsAdmin(), lambda message: not message.text.isdigit(), state=ProductState.price)
async def process_price_invalid(message: Message, state: FSMContext):
    if message.text == back_message:
        await state.set_state(ProductState.image.state)
        await message.answer("Другое изображение?", reply_markup=back_markup())

    else:
        await message.answer('Укажите цену в виде числа!')


@dp.message_handler(IsAdmin(), lambda message: message.text.isdigit(), state=ProductState.price)
async def process_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()
    title = data.get('title')
    body = data.get('body')
    price = data.get('price')
    image = data.get('image')
    await state.set_state(ProductState.confirm.state)
    await message.answer_photo(
        photo=image,
        caption=f'<b>{title}</b>\n\n{body}\n\nЦена: {price} рублей.',
        reply_markup=check_markup(),
    )


@dp.message_handler(IsAdmin(), lambda message: message.text not in (back_message, all_right_message), state=ProductState.confirm)
async def process_confirm_invalid(message: Message, state: FSMContext):
    await message.answer('Такого варианта не было.')


@dp.message_handler(IsAdmin(), text=back_message, state=ProductState.confirm)
async def process_confirm_back(message: Message, state: FSMContext):
    await state.set_state(ProductState.price.state)
    await message.answer(f"Изменить цену с <b>{state.get_data().get('price')}</b>?", reply_markup=back_markup())


@dp.message_handler(IsAdmin(), text=all_right_message, state=ProductState.confirm)
async def process_confirm(message: Message, state: FSMContext):
    data = await state.get_data()
    title = data.get('title')
    body = data.get('body')
    image = data.get('image')
    price = data.get('price')

    with db as conn:
        tag = conn.fetchone(
            'SELECT title FROM categories WHERE idx=?',
            (
                data.get('category_index'),
            )
        )[0]
        idx = md5(' '.join([title, body, price, tag]
                           ).encode('utf-8')).hexdigest()

        conn.query(
            'INSERT INTO products VALUES (?, ?, ?, ?, ?, ?)',
            (idx, title, body, image, int(price), tag)
        )

    await state.finish()
    await message.answer('Готово!', reply_markup=ReplyKeyboardRemove())
    await process_settings(message)


# delete product
@dp.callback_query_handler(IsAdmin(), product_cb.filter(action='delete'))
async def delete_product_callback_handler(callback: CallbackQuery, callback_data: dict):
    product_idx = callback_data['id']
    with db as conn:
        conn.query('DELETE FROM products WHERE idx=?', (product_idx,))
    await callback.answer('Удалено!')
    await callback.message.delete()


async def show_products(msg, products, category_idx):
    await bot.send_chat_action(msg.chat.id, ChatActions.TYPING)

    for idx, title, body, image, price, tag in products:
        text = f'<b>{title}</b>\n\n{body}\n\nЦена: {price} рублей.'

        markup = InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                '🗑️ Удалить',
                callback_data=product_cb.new(
                    id=idx,
                    action='delete'
                )
            )
        )

        await msg.answer_photo(
            photo=image,
            caption=text,
            reply_markup=markup
        )

    markup = InlineKeyboardMarkup().add(add_product, delete_category)
    await msg.answer(f'Хотите что-нибудь добавить или удалить? ', reply_markup=markup)
