import logging
import sqlite3

import config
from middleware.custom import SomeMiddleware


async def on_startup(dp):
    logging.info('new start')
    await dp.bot.set_my_commands(config.COMMANDS)


async def on_shotdown(dp):
    logging.info('end start')

    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute(f"""delete from block_list where user_id={config.ADMINS[0]}""")
        conn.commit()


if __name__ == '__main__':
    from aiogram import executor
    from utils.database import create_table
    from handlers import dp

    create_table()
    dp.middleware.setup(SomeMiddleware())
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shotdown,
    )
