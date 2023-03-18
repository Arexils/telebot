import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import webhook

from config import TOKEN, WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT

logging.basicConfig(level=logging.INFO)
bot = Bot(
    token=TOKEN,
    parse_mode='HTML',
)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


async def on_startup(dp):
    logging.info('Setting webhook :D')
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    logging.info('Shutting down..')
    await bot.delete_webhook()
    logging.info('Bye!')


@dp.message_handler(commands=['start'])
async def command_start(msg: types.Message):
    return webhook.SendMessage(msg.chat.id, 'Добро пожаловать!')


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
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        webhook_path=WEBHOOK_PATH,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
