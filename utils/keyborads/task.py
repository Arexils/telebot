from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class KeyboardMain(ReplyKeyboardMarkup):
    def __init__(self):
        super().__init__(resize_keyboard=True, one_time_keyboard=True)
        self.add(KeyboardButton('Напитки'))
        self.add(KeyboardButton('Закуски'))


class KeyboardDrink(ReplyKeyboardMarkup):
    def __init__(self):
        super().__init__(resize_keyboard=True, one_time_keyboard=True)
        self.add(
            KeyboardButton('Сок'),
            KeyboardButton('Газировка'),
        )
        self.add(KeyboardButton('Назад'))


class KeyboardSnack(ReplyKeyboardMarkup):
    def __init__(self):
        super().__init__(resize_keyboard=True, one_time_keyboard=True)
        self.add(
            KeyboardButton('Чипсы'),
            KeyboardButton('Бургер'),
        )
        self.add(KeyboardButton('Назад'))
