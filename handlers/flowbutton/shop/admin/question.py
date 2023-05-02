from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.types.chat import ChatActions
from aiogram.utils.callback_data import CallbackData

from handlers.flowbutton.shop.filters.filters import IsAdmin
from handlers.flowbutton.shop.keyboards.default import submit_markup
from handlers.flowbutton.shop.keyboards.default.markups import cancel_message, all_right_message
from handlers.flowbutton.shop.shop import AnswerState
from handlers.flowbutton.shop.user.menu import questions
from loader import dp, db, bot

question_cb = CallbackData('question', 'cid', 'action')


@dp.message_handler(IsAdmin(), text=questions)
async def process_questions(msg: Message):
    await msg.answer_chat_action(ChatActions.TYPING)
    with db as conn:
        questions = conn.fetchall('SELECT * FROM questions')

    if len(questions) == 0:
        await msg.answer('Нет вопросов.')

    else:
        for cid, question in questions:
            markup = InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    'Ответить',
                    callback_data=question_cb.new(cid=cid, action='answer')
                )
            )
            await msg.answer(question, reply_markup=markup)


@dp.callback_query_handler(IsAdmin(), question_cb.filter(action='answer'))
async def process_answer(callback: CallbackQuery, callback_data: dict, state: FSMContext):
    await state.update_data(cid=callback_data['cid'])

    await callback.message.answer('Напиши ответ.', reply_markup=ReplyKeyboardRemove())
    await state.set_state(AnswerState.answer.state)


@dp.message_handler(IsAdmin(), state=AnswerState.answer)
async def process_submit(msg: Message, state: FSMContext):
    await state.update_data(answer=msg.text)
    await state.set_state(AnswerState.submit.state)
    await msg.answer('Убедитесь, что не ошиблись в ответе.', reply_markup=submit_markup())


@dp.message_handler(IsAdmin(), text=cancel_message, state=AnswerState.submit)
async def process_send_answer(message: Message, state: FSMContext):
    await message.answer('Отменено!', reply_markup=ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(IsAdmin(), text=all_right_message, state=AnswerState.submit)
async def process_send_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    answer = data['answer']
    cid = data['cid']

    with db as conn:
        question = conn.fetchone(
            'SELECT question FROM questions WHERE cid=?', (cid,))[0]
        conn.query('DELETE FROM questions WHERE cid=?', (cid,))
        text = f'Вопрос: <b>{question}</b>\n\nОтвет: <b>{answer}</b>'

        await message.answer('Отправлено!', reply_markup=ReplyKeyboardRemove())
        await bot.send_message(cid, text)

    await state.finish()
