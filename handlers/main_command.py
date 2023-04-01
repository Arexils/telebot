import sqlite3

from aiogram import types

from loader import dp


@dp.message_handler(commands=['start', ])
async def command_start(msg: types.Message):
    await msg.answer('Ну привет!')
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute(
            f"""
                INSERT INTO chat_message(user_id, chat_id, message) VALUES (?,?,?)
            """,
            (
                msg.from_user.id,
                msg.chat.id,
                msg.text
            )
        )
        conn.commit()
