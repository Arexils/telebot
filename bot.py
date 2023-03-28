import asyncio
import logging
import random
import sqlite3

import requests
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import filters
from aiogram.dispatcher.filters import CommandStart, AdminFilter, IDFilter
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils import markdown

import config
from config import TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=TOKEN,
    parse_mode=types.ParseMode.HTML,
)
dp = Dispatcher(bot)


async def on_startup(dp):
    logging.info('new start')


async def on_shotdown(dp):
    logging.info('end start')


@dp.message_handler(CommandStart())
async def command_start(msg: types.Message):
    await msg.answer('Ну привет!')


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


#
@dp.message_handler(IDFilter(config.ADMINS), commands=['info_2'])
async def command_info_profile_2(msg: types.Message):
    text = markdown.text(
        msg.from_user.mention,
        markdown.text(
            markdown.bold('ID: '),
            markdown.code(msg.from_user.id),
        ),
        markdown.text(
            markdown.bold('Chat ID: '),
            msg.chat.id,
        ),
        sep='\n'
    )
    await msg.answer(text, parse_mode=types.ParseMode.MARKDOWN_V2)


@dp.message_handler(commands=['funny'])
async def command_funny(msg: types.Message):
    response = requests.get('https://aws.random.cat/meow').json().get('file')
    await msg.answer_photo(response)


@dp.message_handler(AdminFilter() | IDFilter(config.ADMINS), commands=['poll'], )
async def send_poll_to_user(message: types.Message):
    poll = {
        'question': 'Перерыв',
        'options': ['Без перерыва', '5 минут', '10 минут'],
        'is_anonymous': True,
    }

    await message.answer_poll(**poll)


@dp.message_handler(commands=['dice'], )
async def dice(msg: types.Message):
    for e in ['🎲', '🎯', '🏀', '⚽', '🎳', '🎰']:
        await msg.answer_dice(e)


@dp.message_handler(
    # filters.Regexp(re.compile(r'\d+')),
    # filters.ForwardedMessageFilter(True),
    content_types=types.ContentType.TEXT,
)
async def echo_msg(msg: types.Message):
    await msg.answer(f'Echo: {msg.text}')


@dp.message_handler(
    content_types=types.ContentType.PHOTO,
)
async def echo_photo(msg: types.Message):
    photo = msg.photo[-1]
    caption = (
        f"<b>Размер:</b> <code>{photo.file_size}</code> kByte\n"
        f"<b>Ширина:</b> <code>{photo.width}</code> px\n"
        f"<b>Высота:</b> <code>{photo.height}</code> px\n"
    )
    await msg.answer('Сейчас обработаю фото!')
    await asyncio.sleep(random.randint(1, 7))
    await msg.answer_photo(
        photo.file_id,
        caption=msg.caption if msg.caption else caption,
    )


class SomeMiddleware(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        print('on_pre_process_update')
        data['middleware_data'] = 'some update data'
        if update.message:
            await update.message.answer('on_pre_process_update')

    async def on_process_update(self, update: types.Update, data: dict):
        print(f'on_process_update, {data=}')

    async def on_pre_process_message(self, message: types.Message, data: dict):
        print(f'on_pre_process_message, {data=}')
        data['middleware_data1'] = 'some message data1'
        user_id = message.from_user.id
        is_blocked = user_id in [1, ]
        print(user_id, is_blocked)
        data['is_blocked'] = is_blocked
        # if user_id in block_users:
        #     await message.answer('ты в бане')
        #     raise CancelHandler()

    async def on_process_message(self, message: types.Message, data: dict):
        print(f'on_process_message, {data=}')
        data['middleware_data2'] = 'some message data2'
        user_id = str(message.from_user.id)
        data['user_id'] = user_id
        data['user'] = '123456'

    async def on_post_process_message(self, message: types.Message, data_from_handler: list, data: dict):
        print(f'on_post_process_message, {data=}, {data_from_handler=}')
        data['middleware_data3'] = 'some message data3'


if __name__ == '__main__':
    from aiogram import executor
    from database import create_table

    create_table()
    dp.middleware.setup(SomeMiddleware())
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shotdown,
    )
