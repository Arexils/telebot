# https://core.telegram.org/bots/api#markdownv2-style
import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.utils.exceptions import BotBlocked

from config import TOKEN

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, parse_mode='MarkdownV2')
dp = Dispatcher(bot)


@dp.errors_handler(exception=BotBlocked)
async def blocked(update: types.Update, exc: BotBlocked):
    print(f'Пользователь кинул в блок. error: {exc}\n {update}')
    return True


@dp.message_handler(commands=['start'])
async def command_start(msg: types.Message):
    await msg.reply('reply')


@dp.message_handler(commands=['help'])
async def command_help(msg: types.Message):
    await msg.answer('Какой\-то *текст* с подсказками')


@dp.message_handler(commands=['test'])
async def command_test(msg: types.Message):
    await asyncio.sleep(10)
    await msg.reply('Какой\-то тест')

@dp.message_handler(commands=['mark'])
async def command_test(msg: types.Message):
    await msg.reply('Какой-то тест')


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def echo(msg: types.Message):
    photo = msg.photo[-1]
    photo_obj = await photo.download()
    await msg.answer_photo('https://www.python.org/static/img/python-logo@2x.png')
    os.remove(photo_obj.name)


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
