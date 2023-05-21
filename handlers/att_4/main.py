import logging

from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, ContentType
from sqlalchemy import select

import config
from handlers.att_4.keyboards import btn_cancel, btn_check, keyboard_sub, btn_premium, btn_basic, btn_vip
from loader import dp, db
from utils.database.model import User, Subscriber


@dp.message_handler(commands='buy_sub')
async def buy_sub(msg: Message):
    id_ = msg.from_user.id
    async with db as session:
        subscriber_query: Subscriber = (await session.scalars(select(Subscriber).join(User).filter_by(user=id_).limit(1))).first()
    if subscriber_query:
        await msg.answer(f'Добро пожаловать {msg.from_user.username}')
    else:
        await msg.answer('Для начала работы вам необходимо подписаться', reply_markup=keyboard_sub)


@dp.callback_query_handler(text=btn_cancel.callback_data)
async def push_cancel(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Вы отказались от подписки\nДля дальнейшей работы с ботом необходима подписка')


@dp.callback_query_handler(text=btn_check.callback_data)
async def check_sub(callback: CallbackQuery):
    await callback.answer()
    async with db as session:
        subscriber_query: Subscriber = (await session.scalars(select(Subscriber).join(User).filter_by(user=callback.from_user.id).limit(1))).first()
    if subscriber_query:
        await callback.message.answer('Подписка активирована')
    else:
        await callback.message.answer(
            'Подписка не активна',
        )


@dp.callback_query_handler(text=btn_basic.callback_data)
async def payment(callback: CallbackQuery):
    await callback.bot.send_invoice(
        chat_id=callback.from_user.id,
        title='Подписка',
        description='Подписка на бота базовая',
        payload='basic',
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
        payload='prem',
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
        payload='vip',
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


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(msg: Message):
    id_user = msg.from_user.id
    async with db as session:
        user: User = (await session.scalars(select(User).filter_by(user=id_user).limit(1))).first()
        new_sub: Subscriber = Subscriber(
            user=user,
            lvl_sub=msg.successful_payment.invoice_payload,
        )
        session.add(new_sub)
        await session.commit()

    await msg.answer('Вы подписались')
    logging.info(f'Новый подписчик {msg.from_user.id}')
