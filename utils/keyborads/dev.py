from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton('1️')
button2 = KeyboardButton('2️')
button3 = KeyboardButton('3️')
button4 = KeyboardButton('4')
button5 = KeyboardButton('5')
button6 = KeyboardButton('6')

kb.add(
   button1, button2, button3, button4, button5, button6
)
kb.row(
   button1, button2, button3, button4, button5, button6
)

kb.row(button4, button2)
kb.add(button3, button2)
kb.insert(button1)
kb.insert(button6)
kb.insert(KeyboardButton('9'))
