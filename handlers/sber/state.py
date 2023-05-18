from aiogram.dispatcher.filters.state import StatesGroup, State


class Help(StatesGroup):
    waiting_message = State()
