import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=TOKEN,
    parse_mode=types.ParseMode.HTML,
)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
