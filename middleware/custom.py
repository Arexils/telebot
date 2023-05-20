import logging
import sqlite3

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Update
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from loader import db
from utils.database.model import User, BlockList


class SomeMiddleware(BaseMiddleware):

    async def on_pre_process_update(self, update: Update, data: dict):
        async with db as session:
            if user_query := (
                    await session.scalars(
                        select(BlockList).options(joinedload(BlockList.user)).filter(BlockList.is_block == True)
                                .join(User).filter_by(user=update.message.from_user.id)
                                .limit(1)
                    )
            ).first():
                logging.info(f'Пользователь {user_query} в ЧС!')
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
