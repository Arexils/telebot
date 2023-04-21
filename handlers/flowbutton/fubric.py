from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import dp
from utils.keyborads.dev_inline import calc_keyboard

callback_numbers = CallbackData('fabnum', 'action')

numbers_kb = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='-1', callback_data=callback_numbers.new(action='decr')),
    InlineKeyboardButton(text='+1', callback_data=callback_numbers.new(action='incr')),
).add(
    InlineKeyboardButton(text='Подтвердить', callback_data=callback_numbers.new('finish')),
)
user_data = {}


async def update_num_text(msg: types.Message, new_value: int):
    # Общая функция для обновления текста с отправкой той же клавиатуры
    await msg.edit_text(f'Укажите число: {new_value}', reply_markup=calc_keyboard())


@dp.message_handler(commands='numbers')
async def cmd_numbers(msg: types.Message):
    user_data[msg.from_user.id] = 0
    await msg.answer('Укажите число: 0', reply_markup=numbers_kb)


@dp.callback_query_handler(callback_numbers.filter(action=['incr', 'decr']))
async def callbacks_num_change_fab(callback: types.CallbackQuery, callback_data: dict):
    user_value = user_data.get(callback.from_user.id, 0)
    action = callback_data['action']

    if action == 'incr':
        user_data[callback.from_user.id] = user_value + 1
        await update_num_text(callback.message, user_value + 1)
    elif action == 'decr':
        user_data[callback.from_user.id] = user_value - 1
        await update_num_text(callback.message, user_value - 1)

    await callback.answer()


@dp.callback_query_handler(callback_numbers.filter(action=['finish']))
async def callbacks_num_finish_fab(callback: types.CallbackQuery):
    user_value = user_data.get(callback.from_user.id, 0)
    await callback.message.edit_text(f'Итого: {user_value}')

    await callback.answer()
