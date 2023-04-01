import sqlite3

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware


class SomeMiddleware(BaseMiddleware):

    async def on_process_message(self, message: types.Message, data: dict):
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute(
                f"""
                INSERT INTO chat_message(user_id, chat_id, message) VALUES (?,?,?)
            """,
                (
                    message.from_user.id,
                    message.chat.id,
                    message.text
                )
            )
            conn.commit()
