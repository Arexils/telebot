import logging
from random import choice

RPS = ['камень', 'ножницы', 'бумага']

# TODO: Для доп ДЗ необходимо оптимизировать данный код
def knd_logic(user_selection):

    if user_selection.lower() in RPS:
        bot_selection = choice(RPS)  # выбор бота

        logging.info(f'бот: {bot_selection}')

        if user_selection == "камень" and bot_selection == "камень":
            result = "ничья"
        elif user_selection == "камень" and bot_selection == "ножницы":
            result = "пользователь"
        elif user_selection == "камень" and bot_selection == "бумага":
            result = "бот"

        if user_selection == "ножницы" and bot_selection == "камень":
            result = "бот"
        elif user_selection == "ножницы" and bot_selection == "ножницы":
            result = "ничья"
        elif user_selection == "ножницы" and bot_selection == "бумага":
            result = "пользователь"

        if user_selection == "бумага" and bot_selection == "камень":
            result = "пользователь"
        elif user_selection == "бумага" and bot_selection == "ножницы":
            result = "бот"
        elif user_selection == "бумага" and bot_selection == "бумага":
            result = "ничья"
        return result, bot_selection
    return None
