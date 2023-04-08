import logging
import sqlite3

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Update


class SomeMiddleware(BaseMiddleware):

    async def on_pre_process_update(self, update: Update, data: dict):
        user_id = update.message.from_user.id
        if update.message.text != '/meow':
            with sqlite3.connect('database.db') as conn:
                cur = conn.cursor()
                user_obj = cur.execute("""select user_id from block_list where user_id=(?)""", (user_id,)).fetchone()
                if user_obj is not None:
                    logging.info(f'Пользователь {user_obj} в ЧС!')
                    raise CancelHandler()

    async def on_process_message(self, message: types.Message, data: dict):
        logging.info(f'{message.from_user.id}: {message.text}')
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
