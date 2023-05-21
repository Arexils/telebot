import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, ContentType

import config
from handlers.att_4.keyboards import keyboard, btn_cancel, btn_check, keyboard_sub, btn_premium, btn_basic, btn_vip
from loader import dp


@dp.message_handler(commands='buy_sub', state='*')
async def buy_sub(msg: Message, state: FSMContext):
    data: dict = await state.get_data()

    id_ = msg.from_user.id
    subscribers = [] if data.get('subscribers', ()) is None else data.get('subscribers', ())
    if id_ in subscribers:
        await msg.answer(f'Добро пожаловать {msg.from_user.username}')
    else:
        await msg.answer('Для начала работы вам необходимо подписаться', reply_markup=keyboard_sub)


@dp.callback_query_handler(text=btn_cancel.callback_data)
async def push_cancel(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Вы отказались от подписки\nДля дальнейшей работы с ботом необходима подписка')


@dp.callback_query_handler(text=btn_check.callback_data, state='*')
async def check_sub(callback: CallbackQuery, state: FSMContext):
    data: dict = await state.get_data()
    subscribers = data.get('subscribers', ())
    await callback.answer()
    if callback.from_user.id in subscribers:
        await callback.message.answer('Подписка активирована')
    else:
        await callback.message.answer(
            'Подписка не активна',
            reply_markup=keyboard,
        )


@dp.callback_query_handler(text=btn_basic.callback_data)
async def payment(callback: CallbackQuery):
    await callback.bot.send_invoice(
        chat_id=callback.from_user.id,
        title='Подписка',
        description='Подписка на бота базовая',
        payload='payment',
        provider_token=config.UKASSA,
        currency='RUB',
        start_parameter='test_bot',
        prices=[
            {'label': 'Руб', 'amount': 10000, },
        ],
    )


@dp.callback_query_handler(text=btn_premium.callback_data)
async def payment(callback: CallbackQuery):
    await callback.bot.send_invoice(
        chat_id=callback.from_user.id,
        title='Подписка',
        description='Подписка на бота прем',
        payload='payment',
        provider_token=config.UKASSA,
        currency='RUB',
        start_parameter='test_bot',
        prices=[
            {'label': 'Руб', 'amount': 20000, },
        ],
    )


@dp.callback_query_handler(text=btn_vip.callback_data)
async def payment(callback: CallbackQuery):
    await callback.bot.send_invoice(
        chat_id=callback.from_user.id,
        title='Подписка',
        description='Подписка на бота вип',
        payload='payment',
        provider_token=config.UKASSA,
        currency='RUB',
        start_parameter='test_bot',
        prices=[
            {'label': 'Руб', 'amount': 30000, },
        ],
    )


@dp.pre_checkout_query_handler()
async def proccess_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT, state='*')
async def process_pay(msg: Message, state: FSMContext):
    if msg.successful_payment.invoice_payload == 'payment':
        await msg.answer('Вы подписались')
        data: dict = await state.get_data()
        subscribers = (data.get('subscribers', []))
        subscribers.append(msg.from_user.id)
        await state.set_data({'subscribers': subscribers, })
        logging.info(f'Новый подписчик {msg.from_user.id}')
