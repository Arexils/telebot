import logging

import config
from middleware.custom import SomeMiddleware
from utils.database.core import engine
from utils.database.model import Base


async def on_startup(dp):
    logging.info('new start')
    await dp.bot.set_my_commands(config.COMMANDS)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def on_shotdown(dp):
    logging.info('end start')
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    dp.middleware.setup(SomeMiddleware())
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shotdown,
    )
