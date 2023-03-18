import logging

import requests
from aiogram import Bot, Dispatcher, types

from config import TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=TOKEN,
    parse_mode='HTML'
)
dp = Dispatcher(bot)


async def on_startup(dp):
    logging.info('new start')


async def on_shotdown(dp):
    logging.info('end start')


@dp.message_handler(
    text='пакет',
    content_types=types.ContentType.TEXT,
)
async def echo(msg: types.Message):
    await msg.answer(msg.text)


@dp.message_handler(commands=['info'])
async def command_info_profile(msg: types.Message):
    text = (
        f'{msg.from_user.mention}\n'
        f'<b>ID: </b> <code>{msg.from_user.id}</code>\n'
        f'<b>Chat ID: </b> {msg.chat.id}\n'
    )
    await msg.answer(text)


@dp.message_handler(commands=['funny'])
async def command_funny(msg: types.Message):
    response = requests.get('https://aws.random.cat/meow').json().get('file')
    await msg.answer_photo(response)


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shotdown,
    )
