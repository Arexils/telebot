import logging

import config
from loader import dp
from middleware.custom import SomeMiddleware


async def on_startup(dp):
    logging.info('new start')
    await dp.bot.set_my_commands(config.COMMANDS)


async def on_shotdown(dp):
    logging.info('end start')


if __name__ == '__main__':
    from aiogram import executor
    from utils.database import create_table
    from handlers import *

    create_table()
    dp.middleware.setup(SomeMiddleware())
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shotdown,
    )
