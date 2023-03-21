import logging
import sqlite3

import requests
from aiogram import Bot, Dispatcher, types

from config import TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=TOKEN,
    parse_mode='HTML'
)
dp = Dispatcher(bot)


async def on_startup(dp):
    logging.info('new start')


async def on_shotdown(dp):
    logging.info('end start')


@dp.message_handler(commands=['fetchone'])
async def command_fetchone(msg: types.Message):
    with sqlite3.connect('database.db') as connection:
        cur = connection.cursor()
        user = cur.execute(f"SELECT * FROM user WHERE user_id={msg.from_user.id}").fetchone()
        logging.info(f'fetchone: {msg.from_user.username} {msg.from_user.id}')
        if user:
            await msg.answer(f'fetchone - {user}')
        else:
            await msg.answer(f'ты не в БД! (Напиши любок сообщение)')


@dp.message_handler(commands=['fetchall'])
async def command_fetchall(msg: types.Message):
    with sqlite3.connect('database.db') as connection:
        cur = connection.cursor()
        user = cur.execute(f"SELECT user_id FROM user").fetchall()
        logging.info(f'fetchall: {msg.from_user.username} {msg.from_user.id}')
        if user:
            await msg.answer(f'fetchall - {user}')
        else:
            await msg.answer(f'ты не в БД! (Напиши любок сообщение)')


@dp.message_handler(commands=['info'])
async def command_info_profile(msg: types.Message):
    text = (
        f'{msg.from_user.mention}\n'
        f'<b>ID: </b> <code>{msg.from_user.id}</code>\n'
        f'<b>Chat ID: </b> {msg.chat.id}\n'
    )
    await msg.answer(text)


@dp.message_handler(commands=['funny'])
async def command_funny(msg: types.Message):
    response = requests.get('https://aws.random.cat/meow').json().get('file')
    await msg.answer_photo(response)


@dp.message_handler(
    content_types=types.ContentType.TEXT,
)
async def echo(msg: types.Message):
    with sqlite3.connect('database.db') as connection:
        cur = connection.cursor()
        user = cur.execute(f"SELECT * FROM user WHERE user_id={msg.from_user.id}").fetchone()
        if not user:
            logging.info(f'Создание нового пользователя: {msg.from_user.username} {msg.from_user.id}')

            data = (msg.from_user.id, msg.chat.id, msg.from_user.username)
            cur.execute(f"INSERT INTO user(user_id, chat_id, username) VALUES (?,?,?)", data)

            connection.commit()
            await msg.answer('Вы добавлены в БД.')

        msg_data = (msg.from_user.id, msg.chat.id, msg.text)
        cur.execute(f"INSERT INTO chat_message(user_id , chat_id, message) VALUES (?,?,?)", msg_data)
        await msg.answer(msg.text)


if __name__ == '__main__':
    from aiogram import executor
    from database import create_table

    create_table()
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shotdown,
    )
