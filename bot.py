import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import webhook

from config import TOKEN

# настройки webhook
WEBHOOK_HOST = 'https://10ed-95-84-236-95.eu.ngrok.io'
WEBHOOK_PATH = ''
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# настройки веб сервера
WEBAPP_HOST = '127.0.0.1'  # or ip
WEBAPP_PORT = 8000

logging.basicConfig(level=logging.INFO)
bot = Bot(
    token=TOKEN,
    parse_mode='HTML',
)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    logging.warning('Shutting down..')
    await bot.delete_webhook()
    logging.warning('Bye!')


@dp.message_handler(commands=['start'])
async def command_start(msg: types.Message):
    return webhook.SendMessage(msg.chat.id, msg.text)


@dp.message_handler(commands=['help'])
async def command_help(msg: types.Message):
    return webhook.SendMessage(msg.chat.id, 'Вы обратились к справке бота')


@dp.message_handler(commands=['myID'])
async def get_id_user(msg: types.Message):
    return webhook.SendMessage(msg.chat.id, f'ID: <code>{msg.chat.id}</code>')


if __name__ == '__main__':
    from aiogram import executor

    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
