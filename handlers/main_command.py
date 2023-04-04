import sqlite3

from aiogram import types

from loader import dp


@dp.message_handler(commands=['start', ])
async def command_start(msg: types.Message):
    user_id = msg.from_user.id
    chat_id = msg.chat.id
    username = msg.from_user.username

    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        user_obj = cur.execute(f"""select user_id from user where user_id={user_id}""").fetchone()

        if not user_obj:
            cur.execute(
                f"""
                    INSERT INTO user(user_id,chat_id, username) VALUES (?,?,?)
                """,
                (
                    user_id,
                    chat_id,
                    username,
                )
            )
            conn.commit()
            await msg.answer('Добро пожаловать!')
        else:
            await msg.answer('Ну привет!')
