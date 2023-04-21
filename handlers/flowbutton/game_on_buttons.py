import logging
import re
from random import randint

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.callback_data import CallbackData

from loader import dp

secret_number: int | None = None
attempts: int = 0

game_random_callback = CallbackData('game_random', 'action')

button_start = InlineKeyboardButton('Начать', callback_data=game_random_callback.new('start'))
button_cancel = InlineKeyboardButton('Отмена', callback_data=game_random_callback.new('cancel'))
start_menu = InlineKeyboardMarkup(resize_keyboard=True).add(
    button_start,
    button_cancel,
)


def random_num():
    global secret_number
    secret_number = randint(1, 10)
    logging.info(f'Бот загадал {secret_number}')
    return secret_number


@dp.message_handler(commands='start_random_game')
async def start_random_game(msg: Message):
    await msg.answer(
        (
            'Привет! Это игра угадай число!\n'
            'Для старта игры нажми на кнопку начать'
        ),
        reply_markup=start_menu)


@dp.callback_query_handler(game_random_callback.filter(action='cancel'))
async def end_game_command(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer(callback.id)


@dp.callback_query_handler(game_random_callback.filter(action='start'))
async def start_game_command(callback: CallbackQuery):
    global secret_number, attempts
    attempts = 3
    secret_number = random_num()
    await callback.message.answer('Я загадал число от 1 до 10\nПопробуй угадай его')
    await callback.answer(callback.id)
    await callback.message.delete()
    logging.info(secret_number)


@dp.message_handler(regexp=re.compile(r'^\d+$'))
async def check_numbers(msg: Message):
    global secret_number, attempts
    user_number = int(msg.text)
    attempts -= 1

    if attempts < 1:
        await msg.reply('Вы проиграли', reply_markup=start_menu)
        return

    if secret_number is not None:
        if user_number > secret_number:
            await msg.reply(f'Секретное число меньше.\nКоличество попыток: {attempts}')
        elif user_number < secret_number:
            await msg.reply(f'Секретное число больше.\nКоличество попыток: {attempts}')
        else:
            await msg.reply('Вы угадали!\nНачать заново?', reply_markup=start_menu)
            secret_number = None
            attempts = 0
            return
    else:
        await msg.reply('Для начала игры введите /start_random_game')
