import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ChatActions, ReplyKeyboardMarkup, CallbackQuery, ReplyKeyboardRemove

from handlers.flowbutton.shop.filters.filters import IsUser
from handlers.flowbutton.shop.keyboards.default import check_markup
from handlers.flowbutton.shop.keyboards.default.markups import all_right_message, back_message, back_markup, confirm_markup, confirm_message
from handlers.flowbutton.shop.keyboards.inline.products_from_cart import product_markup, product_cb
from handlers.flowbutton.shop.shop import CheckoutState
from handlers.flowbutton.shop.user.menu import cart
from loader import dp, db


@dp.message_handler(IsUser(), text=cart)
async def process_cart(msg: Message, state: FSMContext):
    with db as conn:
        cart_data = conn.fetchall(
            'SELECT * FROM cart WHERE cid=?',
            (msg.chat.id,)
        )

        if len(cart_data) == 0:
            await msg.answer('Ваша корзина пуста.')
        else:
            await msg.answer_chat_action(ChatActions.TYPING)
            await state.update_data(products={})
            order_cost = 0
            for _, idx, count_in_cart in cart_data:
                product = conn.fetchone('SELECT * FROM products WHERE idx=?', (idx,))
                if product is None:
                    conn.query('DELETE FROM cart WHERE idx=?', (idx,))
                else:
                    _, title, body, image, price, _ = product
                    order_cost += price
                    await state.update_data(products={idx: [title, price, count_in_cart]})
                    markup = product_markup(idx, count_in_cart)
                    text = f'<b>{title}</b>\n\n{body}\n\nЦена: {price}₽.'

                    await msg.answer_photo(
                        photo=image,
                        caption=text,
                        reply_markup=markup
                    )

            if order_cost != 0:
                markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                markup.add('📦 Оформить заказ')

                await msg.answer(
                    'Перейти к оформлению?',
                    reply_markup=markup
                )


@dp.callback_query_handler(IsUser(), product_cb.filter(action=['count', 'increase', 'decrease']))
async def product_callback_handler(callback: CallbackQuery, callback_data: dict, state: FSMContext):
    idx = callback_data['id']
    action = callback_data['action']

    data = await state.get_data()
    if 'count' == action:
        if 'products' not in data.keys():
            await process_cart(callback.message, state)
        else:
            await callback.answer(f'Количество - {data["products"][idx][2]}')
    else:
        if 'products' not in data.keys():
            await process_cart(callback.message, state)
        else:
            data['products'][idx][2] += 1 if 'increase' == action else -1
            count_in_cart = data['products'][idx][2]
            with db as conn:
                if count_in_cart == 0:
                    conn.query(
                        """
                        DELETE FROM cart
                            WHERE cid = ? AND idx = ?
                        """,
                        (
                            callback.message.chat.id,
                            idx
                        )
                    )
                    await callback.message.delete()
                else:
                    conn.query(
                        """
                        UPDATE cart
                           SET quantity = ?
                           WHERE cid = ? AND idx = ?
                   """,
                        (
                            count_in_cart,
                            callback.message.chat.id,
                            idx
                        )
                    )
                    await callback.message.edit_reply_markup(product_markup(idx, count_in_cart))


@dp.message_handler(IsUser(), text='📦 Оформить заказ')
async def process_checkout(msg: Message, state: FSMContext):
    await state.set_state(CheckoutState.check_cart.state)
    await checkout(msg, state)


async def checkout(msg: Message, state):
    answer = ''
    total_price = 0
    data = await state.get_data()
    for title, price, count_in_cart in data['products'].values():
        tp = count_in_cart * price
        answer += f'<b>{title}</b> * {count_in_cart}шт. = {tp}₽\n'
        total_price += tp

    await msg.answer(
        f'{answer}\nОбщая сумма заказа: {total_price}₽.',
        reply_markup=check_markup()
    )


@dp.message_handler(IsUser(), lambda msg: msg.text not in [all_right_message, back_message], state=CheckoutState.check_cart)
async def process_check_cart_invalid(msg: Message):
    await msg.reply('Такого варианта не было.')


@dp.message_handler(IsUser(), text=back_message, state=CheckoutState.check_cart)
async def process_check_cart_back(msg: Message, state: FSMContext):
    await state.finish()
    await process_cart(msg, state)


@dp.message_handler(IsUser(), text=all_right_message, state=CheckoutState.check_cart)
async def process_check_cart_all_right(msg: Message, state: FSMContext):
    await state.set_state(CheckoutState.name.state)
    await msg.answer(
        'Укажите свое имя.',
        reply_markup=back_markup()
    )


@dp.message_handler(IsUser(), text=back_message, state=CheckoutState.name)
async def process_name_back(message: Message, state: FSMContext):
    await CheckoutState.check_cart.set()
    await checkout(message, state)


@dp.message_handler(IsUser(), state=CheckoutState.name)
async def process_name(msg: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(name=msg.text)
    if 'address' in data.keys():
        await confirm(msg)
        await state.set_state(CheckoutState.confirm.state)
    else:
        await state.set_state(CheckoutState.address.state)
        await msg.answer(
            'Укажите свой адрес места жительства.',
            reply_markup=back_markup()
        )


@dp.message_handler(IsUser(), text=back_message, state=CheckoutState.address)
async def process_address_back(msg: Message, state: FSMContext):
    data = await state.get_data()
    await msg.answer(
        f'Изменить имя с <b> {data["name"]} </b>?',
        reply_markup=back_markup()
    )
    await state.set_state(CheckoutState.name.state)


@dp.message_handler(IsUser(), state=CheckoutState.address)
async def process_address(msg: Message, state: FSMContext):
    await state.update_data(address=msg.text)
    await confirm(msg)
    await state.set_state(CheckoutState.confirm.state)


async def confirm(msg: Message):
    await msg.answer(
        'Убедитесь, что все правильно оформлено и подтвердите заказ.',
        reply_markup=confirm_markup()
    )


@dp.message_handler(IsUser(), lambda msg: msg.text not in [confirm_message, back_message], state=CheckoutState.confirm)
async def process_confirm_invalid(msg: Message):
    await msg.reply('Такого варианта не было.')


@dp.message_handler(IsUser(), text=back_message, state=CheckoutState.confirm)
async def process_confirm(msg: Message, state: FSMContext):
    await state.set_state(CheckoutState.address.state)
    data = await state.get_data()
    await msg.answer(
        f'Изменить адрес с <b> {data["address"]} </b>?',
        reply_markup=back_markup()
    )


@dp.message_handler(IsUser(), text=confirm_message, state=CheckoutState.confirm)
async def process_confirm(msg: Message, state: FSMContext):
    enough_money = True
    markup = ReplyKeyboardRemove()
    if enough_money:
        logging.info('Deal was made.')
        with db as conn:
            data = await state.get_data()
            cid = msg.chat.id
            products = [
                idx + '=' + str(quantity)
                for idx, quantity in conn.fetchall(
                    """
                    SELECT idx, quantity 
                    FROM cart
                    WHERE cid=?
                    """,
                    (cid,)
                )
            ]  # idx=quantity

            conn.query(
                'INSERT INTO orders VALUES (?, ?, ?, ?)',
                (
                    cid,
                    data['name'],
                    data['address'],
                    ' '.join(products)
                )
            )

            conn.query('DELETE FROM cart WHERE cid=?', (cid,))
            await msg.answer(
                f'Ок! Ваш заказ уже в пути 🚀\nИмя: <b> {data["name"]} </b>\nАдрес: <b> {data["address"]}  </b>',
                reply_markup=markup)
    else:
        await msg.answer('У вас недостаточно денег на счете. Пополните баланс!',
                         reply_markup=markup)
    await state.finish()
