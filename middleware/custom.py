import logging
import sqlite3

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Update


class SomeMiddleware(BaseMiddleware):

    async def on_pre_process_update(self, update: Update, data: dict):
        user_id = update.message.from_user.id
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            user_obj = cur.execute(f"""select user_id from block_list where user_id={user_id}""").fetchone()
            if user_obj:
                logging.info('...')
                raise ...

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
