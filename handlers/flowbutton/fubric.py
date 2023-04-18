from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import dp

callback_numbers = CallbackData('fabnum', 'action')

numbers_kb = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='-1', callback_data=callback_numbers.new(action='decr')),
    InlineKeyboardButton(text='+1', callback_data=callback_numbers.new(action='incr')),
).add(
    InlineKeyboardButton(text='Подтвердить', callback_data=callback_numbers.new('finish')),
)
user_data = {}


async def update_num_text(message: types.Message, new_value: int):
    # Общая функция для обновления текста с отправкой той же клавиатуры
    await message.edit_text(f'Укажите число: {new_value}', reply_markup=calc_keyboard())


@dp.message_handler(commands='numbers')
async def cmd_numbers(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer('Укажите число: 0', reply_markup=numbers_kb)


@dp.callback_query_handler(callback_numbers.filter(action=['incr', 'decr']))
async def callbacks_num_change_fab(call: types.CallbackQuery, callback_data: dict):
    user_value = user_data.get(call.from_user.id, 0)
    action = callback_data['action']
    if action == 'incr':
        user_data[call.from_user.id] = user_value + 1
        await update_num_text(call.message, user_value + 1)
    elif action == 'decr':
        user_data[call.from_user.id] = user_value - 1
        await update_num_text(call.message, user_value - 1)

    await call.answer()


@dp.callback_query_handler(callback_numbers.filter(action=['finish']))
async def callbacks_num_finish_fab(call: types.CallbackQuery):
    user_value = user_data.get(call.from_user.id, 0)
    await call.message.edit_text(f'Итого: {user_value}')

    await call.answer()
