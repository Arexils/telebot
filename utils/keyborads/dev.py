from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# button1 = KeyboardButton('1️')
# button2 = KeyboardButton('2️')
# button3 = KeyboardButton('3️')

# kb = ReplyKeyboardMarkup() \
#     .add(button1) \
#     .add(button2) \
#     .add(button3)

# kb = ReplyKeyboardMarkup().row(button1, button2, button3)

# kb = ReplyKeyboardMarkup().row(
#    button1, button2, button3
# ).add(KeyboardButton('Средний ряд'))
#
# button4 = KeyboardButton('4')
# button5 = KeyboardButton('5')
# button6 = KeyboardButton('6')
# kb.row(button4, button5)
# kb.insert(button6)

kb = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отправить свой контакт', request_contact=True)
).add(
    KeyboardButton('Отправить свою локацию', request_location=True)
)
