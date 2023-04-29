import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN
from utils.database import DatabaseManager

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=TOKEN,
    parse_mode=types.ParseMode.HTML,
)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = DatabaseManager('database.db')
