import datetime

from aiogram import types
from aiogram.types import Message
from sqlalchemy import select

from loader import dp, bot, db
from utils.database.model import User


# срабатывает при появлении нового пользователя
@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_member(msg: Message):
    async with db as session:
        if (await session.scalars(select(User).filter_by(user=msg.from_user.id).limit(1))).first() is None:
            user = User(
                user=msg.from_user.id,
                note=f'{datetime.datetime.now()}'
            )
            session.add(user)
            await session.commit()

    await msg.reply(f'Привет {msg.new_chat_members[0].full_name}')


# пользователь удалил наш бот
@dp.message_handler(content_types=types.ContentType.LEFT_CHAT_MEMBER)
async def banned_member(msg: Message):
    if msg.left_chat_member.id == msg.from_user.id:  # пользователь сам покинул наш чат
        await msg.answer(f'{msg.left_chat_member.get_mention(as_html=True)} вышел из чата')
    elif msg.from_user.id == (await bot.me).id:  # пользователь удален ботом
        return
    else:  # пользователь покинул нашу группу
        await msg.reply(
            f'{msg.left_chat_member.full_name} был удален из чата пользователем {msg.from_user.get_mention(as_html=True)}'
        )
