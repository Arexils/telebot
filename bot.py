import logging

from aiogram import Bot, Dispatcher, types

from config import TOKEN

logging.basicConfig(level=logging.INFO)
proxy_url = 'http://proxy.server:3128'
bot = Bot(token=TOKEN, proxy=proxy_url)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def command_start(msg: types.Message):
    await msg.answer('Hello! :)')


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
