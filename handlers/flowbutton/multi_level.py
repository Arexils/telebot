from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from aiogram.utils.callback_data import CallbackData

from loader import dp

multi_lvl_callback = CallbackData('multi_kb', 'action')

next_btn = InlineKeyboardButton('Вперед', callback_data=multi_lvl_callback.new('next'))
prev_btn = InlineKeyboardButton('Назад', callback_data=multi_lvl_callback.new('prev'))
close_btn = InlineKeyboardButton('Закрыть', callback_data=multi_lvl_callback.new('close'))
general_btn = InlineKeyboardButton('На главную', callback_data=multi_lvl_callback.new('general'))


def get_inline_kb():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton('1', callback_data=multi_lvl_callback.new('1')),
        InlineKeyboardButton('2', callback_data=multi_lvl_callback.new('2')),
    )


def get_general_kb():
    return InlineKeyboardMarkup().add(
        next_btn,
        prev_btn,
    ).add(
        close_btn,
    )


def get_next_kb():
    return InlineKeyboardMarkup().add(
        next_btn,
        close_btn,
    ).add(
        general_btn,
    )


def get_prev_kb():
    return InlineKeyboardMarkup().add(
        prev_btn,
        close_btn,
    ).add(
        general_btn,
    )


@dp.message_handler(commands='multi_lvl_kb')
async def multilevel(msg: Message):
    await msg.answer('inline', reply_markup=get_inline_kb())


@dp.callback_query_handler(multi_lvl_callback.filter(action=['1', '2', ]))
async def numbers_callback(callback: CallbackQuery, callback_data: dict):
    action = callback_data['action']
    await callback.answer(action)
    await callback.message.edit_text(
        f'выбрано {action}',
        reply_markup=get_general_kb(),
    )


@dp.callback_query_handler(multi_lvl_callback.filter(action=['prev', 'next', ]))
async def action_callback(callback: CallbackQuery, callback_data: dict):
    action = callback_data['action']
    await callback.answer(action)
    await callback.message.edit_text(
        f'выбрано {action}',
        reply_markup=get_next_kb() if action == 'prev' else get_prev_kb()
    )


@dp.callback_query_handler(multi_lvl_callback.filter(action=['close', ]))
async def action_callback(callback: CallbackQuery, callback_data: dict):
    action = callback_data['action']
    await callback.answer(action)

    # Удаление клавиатуры
    await callback.message.edit_reply_markup()
    '------- ИЛИ -------'
    await callback.message.edit_text(
        f'Удалена клавиатура',
        reply_markup=None,
    )


@dp.callback_query_handler(multi_lvl_callback.filter(action=['general', ]))
async def action_callback(callback: CallbackQuery, callback_data: dict):
    action = callback_data['action']
    await callback.answer(action)

    # Удаление клавиатуры
    # await callback.message.edit_reply_markup()
    '------- ИЛИ -------'
    await callback.message.edit_text(
        f'Переход на главную',
        reply_markup=get_inline_kb(),
    )
