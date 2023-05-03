from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

import config
from loader import dp

user_button = InlineKeyboardButton('Пользователь', callback_data='menu')
admin_button = InlineKeyboardButton('Админ', callback_data='menu')


class CheckoutState(StatesGroup):
    check_cart = State()
    name = State()
    address = State()
    confirm = State()


class ProductState(StatesGroup):
    title = State()
    body = State()
    image = State()
    price = State()
    confirm = State()


class CategoryState(StatesGroup):
    title = State()


class HelpState(StatesGroup):
    question = State()
    submit = State()


class AnswerState(StatesGroup):
    answer = State()
    submit = State()


@dp.message_handler(commands='shop')
async def cmd_start(message: types.Message):
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup().row(user_button)
    if message.from_user.id in config.ADMINS:
        markup.insert(admin_button)

    await message.answer(
        (
            'Привет! 👋'
            '🤖 Я бот-магазин по продаже товаров любой категории.'
            '🛍️ Чтобы перейти в каталог и выбрать приглянувшиеся товары воспользуйтесь кнопкой.'
            '💰 Пополнить счет можно через Яндекс.кассу, Сбербанк или Qiwi.'
            '❓ Возникли вопросы? Не проблема! Команда /help_shop поможет связаться с админами, которые постараются как можно быстрее откликнуться.'
        ),
        reply_markup=markup)


# @dp.callback_query_handler(text=user_button.callback_data)
# async def user_mode(callback: CallbackQuery):
#     cid = callback.callback.chat.id
#     if cid in config.ADMINS:
#         config.ADMINS.remove(cid)
#     await callback.answer('Включен пользовательский режим.')
#     await callback.callback.answer('Включен пользовательский режим.', reply_markup=menu_keyboard)
#
#
# @dp.callback_query_handler(text=admin_button.callback_data)
# async def admin_mode(callback: CallbackQuery):
#     cid = callback.callback.chat.id
#     if cid not in config.ADMINS:
#         config.ADMINS.append(cid)
#     await callback.answer('Включен админ режим.')
#     await callback.callback.answer('Включен админ режим.', reply_markup=menu_keyboard)
