import logging
import sqlite3

from aiogram import types

from loader import dp


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
