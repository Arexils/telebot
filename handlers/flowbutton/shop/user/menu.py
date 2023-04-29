from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from handlers.flowbutton.shop.filters.filters import IsAdmin, IsUser
from handlers.flowbutton.shop.shop import admin_button, user_button
from loader import dp

catalog = InlineKeyboardButton('🛍️ Каталог', callback_data='catalog')
balance = InlineKeyboardButton('💰 Баланс', callback_data='balance')
cart = InlineKeyboardButton('🛒 Корзина', callback_data='cart')
delivery_status = InlineKeyboardButton('🚚 Статус заказа', callback_data='delivery_status')

settings = InlineKeyboardButton('⚙️ Настройка каталога', callback_data='settings')
orders = InlineKeyboardButton('🚚 Заказы', callback_data='orders')
questions = InlineKeyboardButton('❓ Вопросы', callback_data='questions')


@dp.callback_query_handler(IsUser(), text=user_button.callback_data)
async def user_menu(callback: CallbackQuery):
    await callback.message.edit_text('Меню', reply_markup=InlineKeyboardMarkup().add(catalog).add(balance, cart).add(delivery_status))


@dp.callback_query_handler(IsAdmin(), text=admin_button.callback_data)
async def admin_menu(callback: CallbackQuery):
    await callback.message.edit_text('Меню', reply_markup=InlineKeyboardMarkup().add(settings).add(questions, orders))
