import logging

from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, ContentType

import config
from handlers.ukassa.keyboards import keyboard, btn_cancel, keyboard_check, btn_check, btn_payment
from loader import dp

subscribers = []


@dp.message_handler(commands='ukassa')
async def ukassa(msg: Message):
    id_ = msg.from_user.id
    if id_ in subscribers or id_ in config.ADMINS:
        await msg.answer(f'Добро пожаловать {msg.from_user.username}', reply_markup=keyboard)
    else:
        await msg.answer('Для начала работы вам необходимо подписаться')


@dp.callback_query_handler(text=btn_cancel.callback_data)
async def push_cancel(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Вы отказались от подписки\nДля дальнейшей работы с ботом необходима подписка')


@dp.message_handler(commands='help')
async def help_message(msg: Message):
    await msg.answer(
        (
            'Вы находитесь в информационном боте\n'
            'Для взаимодействия с ботом необходима подписка\n'
            'Если вы оформили подписку и она не активна напишите пожалуйста администраторам @логин'
        ),
        reply_markup=keyboard_check,
    )


@dp.callback_query_handler(text=btn_check.callback_data)
async def check_sub(callback: CallbackQuery):
    await callback.answer()
    id_ = callback.from_user.id
    if id_ in config.ADMINS:
        await callback.message.answer('Вы являетесь администратором')
    elif id_ in subscribers:
        await callback.message.answer('Подписка активирована')
    else:
        await callback.message.answer(
            'Подписка не активна',
            reply_markup=keyboard,
        )


@dp.callback_query_handler(text=btn_payment.callback_data)
async def payment(callback: CallbackQuery):
    await callback.bot.send_invoice(
        chat_id=callback.from_user.id,
        title='Подписка',
        description='Подписка на бота',
        payload='payment',
        provider_token=config.UKASSA,
        currency='RUB',
        start_parameter='test_bot',
        prices=[
            {'label': 'Руб', 'amount': 10000, },
        ],
    )


@dp.pre_checkout_query_handler()
async def proccess_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(msg: Message):
    if msg.successful_payment.invoice_payload == 'payment':
        await msg.answer('Вы подписались')
        subscribers.append(msg.from_user.id)
        logging.info(f'Обновленный список {subscribers}')
