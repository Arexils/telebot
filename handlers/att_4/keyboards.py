from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

btn_payment = InlineKeyboardButton('Оплатить', callback_data='payment')
btn_cancel = InlineKeyboardButton('Отмена', callback_data='cancel')

keyboard = InlineKeyboardMarkup().add(btn_payment, btn_cancel)

btn_check = InlineKeyboardButton('Проверить подписку', callback_data='check')
keyboard_check = InlineKeyboardMarkup().add(btn_check)

# 1111 1111 1111 1026, 12/22, 000

btn_basic = InlineKeyboardButton('BASIC', callback_data='basic')
btn_premium = InlineKeyboardButton('PREMIUM', callback_data='premium')
btn_vip = InlineKeyboardButton('VIP', callback_data='vip')

keyboard_sub = InlineKeyboardMarkup().add(btn_basic, btn_premium, btn_vip, )
