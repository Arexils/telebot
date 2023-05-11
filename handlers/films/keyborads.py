from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

btn_search = InlineKeyboardButton('Случайный фильм', callback_data='random')
btn_reviews = InlineKeyboardButton('Отзывы', callback_data='reviews')

main_menu = InlineKeyboardMarkup().add(btn_search, btn_reviews)

btn_new_film = InlineKeyboardButton('Другой фильм', callback_data='random')
randon_film_kb = InlineKeyboardMarkup().add(btn_new_film)
