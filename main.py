import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import webhook

from config import TOKEN, WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT

logging.basicConfig(level=logging.INFO)

bot: Bot = Bot(
    token=TOKEN,
    parse_mode=types.ParseMode.HTML,
)
dp: Dispatcher = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


async def on_startup(dp: Dispatcher):
    logging.info('Setting webhook :D')
    await dp.bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp: Dispatcher):
    logging.info('Shutting down..')
    await dp.bot.delete_webhook()
    logging.info('Bye!')


@dp.message_handler(commands=['start'])
async def command_start(msg: types.Message):
    return webhook.SendMessage(msg.chat.id, 'Добро пожаловать!')


@dp.message_handler(commands=['help'])
async def command_help(msg: types.Message):
    return webhook.SendMessage(msg.chat.id, 'Вы обратились к справке бота')


@dp.message_handler(commands=['info'])
async def user_info(msg: types.Message):
    text = (
        f'{msg.from_user.mention}\n'
        f'<b>ID: </b> <code>{msg.from_user.id}</code>\n'
        f'<b>Chat ID: </b> {msg.chat.id}\n'
    )
    return webhook.SendMessage(msg.chat.id, text)


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
