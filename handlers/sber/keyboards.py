from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

button1 = InlineKeyboardButton('Файл 1', callback_data='file1')
button_cnl = InlineKeyboardButton('Отмена', callback_data='cancel')
main_keyboard = InlineKeyboardMarkup().add(button1).add(button_cnl)

btn_help = InlineKeyboardButton('Помощь', callback_data='help')
keyboard_help = InlineKeyboardMarkup().add(btn_help, button_cnl)
