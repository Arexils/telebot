from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, ContentType

import config
from handlers.sber.keyboards import main_keyboard, keyboard_help
from handlers.sber.state import Help
from loader import dp


@dp.message_handler(commands=['sber'])
async def cmd_start(msg: Message):
    await msg.answer(
        (
            f'Здравствуйте {msg.from_user.username}!\n'
            f'Для покупки выберите необходимый вариант ниже'
        ),
        reply_markup=main_keyboard
    )


@dp.message_handler(commands=['help'])
async def cmd_help(msg: Message):
    await msg.answer(
        f'Выберите необходимое действие!',
        reply_markup=keyboard_help
    )


@dp.callback_query_handler(text='cancel')
async def cancel(callback: CallbackQuery):
    await callback.bot.delete_message(callback.from_user.id, callback.message.message_id)


@dp.callback_query_handler(text='help')
async def call_help(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('Напишите вашу проблему')
    await state.set_state(Help.waiting_message.state)


@dp.message_handler(state=Help.waiting_message)
async def send_msg(msg: Message, state: FSMContext):
    await msg.bot.send_message(
        config.ADMINS[0],
        (
            f'Вам сообщение от {msg.from_user.username}\n'
            f'{msg.text}'
        )
    )
    await state.finish()


@dp.callback_query_handler(text='file1')
async def payment(callback: CallbackQuery):
    await callback.bot.send_invoice(
        chat_id=callback.from_user.id,
        title='Покупка',
        description='Покупка файла 1',
        payload='payment',
        provider_token=config.SBER,
        currency='RUB',
        start_parameter='test_bot',
        prices=[
            {'label': 'Руб', 'amount': 10000},
        ],
    )


@dp.pre_checkout_query_handler()
async def proccess_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.bot.answer_pre_checkout_query(
        pre_checkout_query.id,
        ok=True,
    )


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(msg: Message):
    if msg.successful_payment.invoice_payload == 'payment':
        await msg.reply_document(
            open('handlers/sber/file1.txt', 'rb+'),  # тут задать путь к файлу где он находится
            caption='Вы купили файл',
        )
