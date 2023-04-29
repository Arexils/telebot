from aiogram.types import ReplyKeyboardMarkup

back_message = '👈 Назад'
confirm_message = '✅ Подтвердить заказ'
all_right_message = '✅ Все верно'
cancel_message = '🚫 Отменить'


def confirm_markup():
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        selective=True,
    ).add(
        confirm_message
    ).add(back_message)


def back_markup():
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        selective=True,
    ).add(back_message)


def check_markup():
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        selective=True,
    ).row(back_message, all_right_message)


def submit_markup():
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        selective=True,
    ).row(cancel_message, all_right_message)
