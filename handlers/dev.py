from aiogram import types
from sqlalchemy import select
from sqlalchemy.orm import configure_mappers
from sqlalchemy.orm import selectinload

from loader import dp, db
from utils.database.model import User, BlockList


@dp.message_handler(commands=['dev', ])
async def command_dev(msg: types.Message):
    async with db as session:
        if user := (await session.scalars(select(User).filter_by(user=msg.from_user.id).limit(1))).first():
            session.add(BlockList(user_id=user.id, is_block=True, reason='По приколу'))
        else:
            session.add(User(user=msg.from_user.id, note='Lf!'))

        await session.commit()
    await msg.reply(f'Привет')


@dp.message_handler(commands=['del_row', ])
async def command_dev(msg: types.Message):
    async with db as session:
        user: User = (await session.scalars(select(User).filter_by(user=msg.from_user.id).limit(1))).first()
        await session.delete(user)
        await session.commit()
    await msg.reply(f'Привет')


@dp.message_handler(commands=['select', ])
async def command_dev(msg: types.Message):
    async with db as session:
        configure_mappers()
        user: User = (await session.scalars(select(User).options(selectinload(User.block_list)).filter_by(user=msg.from_user.id).limit(1))).first()
        await msg.reply(f'Привет {user.block_list}')
