import sqlite3

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ReplyKeyboardRemove, CallbackQuery

from loader import dp


class CallbackOnStart(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()


def towers():
    list_button_name = (
        ('Москва', 'Санкт Петербург', 'Нижний Новгород', 'Ростов'),
        ('Новосибирск', 'Екатеринбург', 'Казань', 'Челябинск'),
    )

    buttons_list = []
    for item in list_button_name:
        l = []
        for i in item:
            l.append(
                InlineKeyboardButton(
                    text=i,
                    callback_data=i
                )
            )
        buttons_list.append(l)

    keyboard_inline_buttons = InlineKeyboardMarkup(inline_keyboard=buttons_list)
    return keyboard_inline_buttons


@dp.message_handler(commands='state_polling', state='*')
async def on_start_test(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        user_id_obj = cur.execute(
            f"""
            select user_id from polling where user_id={user_id} and vote is 1
        """
        ).fetchone()

        if user_id_obj is None:
            await msg.answer('Описание опросника')
            await msg.answer(
                (
                    'Вопрос №1\n'
                    'Сколько вам лет?\n'
                    'Напишите ответ (только число)'
                ),
                reply_markup=ReplyKeyboardRemove(),
            )
            await state.set_state(CallbackOnStart.Q1.state)
        else:
            await msg.answer(text="Вы уже проходили тест")


@dp.message_handler(state=CallbackOnStart.Q1)
async def tower(msg: Message, state: FSMContext):
    await state.update_data(age=msg.text)
    await msg.answer(
        (
            'Вопрос №2\n'
            'В каком городе вы живете?\n'
            'Выберите ответ из предложенных'
        ),
        reply_markup=towers(),
    )
    await state.set_state(CallbackOnStart.Q2.state)


@dp.callback_query_handler(state=CallbackOnStart.Q2)
async def end(callback: CallbackQuery, state: FSMContext):
    await state.update_data(
        full_name=callback.from_user.full_name,
        city=callback.data,
    )

    data = await state.get_data()
    line_break = '\n\n'
    await callback.message.answer(text=(
        f'Ваши ответы:\n'
        f'{line_break.join(data.values())}'
    ), reply_markup=ReplyKeyboardRemove())

    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute(
            """
                insert into polling(user_id, vote, data) VALUES (?,?,?)
            """,
            (callback.from_user.id, 1, str(data)),
        )
    await state.finish()
