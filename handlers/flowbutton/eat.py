from aiogram import types

from loader import dp
from utils.keyborads.dev import kb
from utils.keyborads.task import KeyboardDrink, KeyboardSnack, KeyboardMain


@dp.message_handler(commands=['dev', ])
async def command_start(msg: types.Message):
    await msg.answer('Тектс', reply_markup=kb)


@dp.message_handler(text='Напитки')
async def get_drink(message: types.Message):
    await message.answer('Выберите напиток', reply_markup=KeyboardDrink())


@dp.message_handler(text='Закуски')
async def get_drink(message: types.Message):
    await message.answer('Выберите закуску', reply_markup=KeyboardSnack())


@dp.message_handler(text='Назад')
async def get_drink(message: types.Message):
    await message.answer('Вы вышли в главное меню', reply_markup=KeyboardMain())
