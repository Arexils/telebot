from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from handlers.flowbutton.shop.keyboards.default import submit_markup
from handlers.flowbutton.shop.keyboards.default.markups import cancel_message, all_right_message
from handlers.flowbutton.shop.shop import HelpState
from loader import dp, db


@dp.message_handler(commands='help_shop')
async def help_shop(msg: Message, state: FSMContext):
    await state.set_state(HelpState.question.state)
    await msg.answer(
        'В чем суть проблемы? Опишите как можно детальнее и администратор обязательно вам ответит.',
        reply_markup=ReplyKeyboardRemove()
    )


@dp.message_handler(state=HelpState.question)
async def process_question(msg: Message, state: FSMContext):
    await state.update_data(question=msg.text)
    await msg.answer('Убедитесь, что все верно.', reply_markup=submit_markup())
    await state.set_state(HelpState.submit.state)


@dp.message_handler(lambda msg: msg.text not in [cancel_message, all_right_message], state=HelpState.submit)
async def process_price_invalid(msg: Message):
    await msg.answer('Такого варианта не было.')


@dp.message_handler(text=cancel_message, state=HelpState.submit)
async def process_cancel(msg: Message, state: FSMContext):
    await msg.answer('Отменено!', reply_markup=ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(text=all_right_message, state=HelpState.submit)
async def process_submit(msg: Message, state: FSMContext):
    cid = msg.chat.id

    with db as conn:
        if conn.fetchone('SELECT * FROM questions WHERE cid=?', (cid,)) is None:
            conn.query(
                'INSERT INTO questions VALUES (?, ?)',
                (
                    cid,
                    (await state.get_data()).get('question')
                )
            )
            await msg.answer('Отправлено!', reply_markup=ReplyKeyboardRemove())

        else:
            await msg.answer('Превышен лимит на количество задаваемых вопросов.', reply_markup=ReplyKeyboardRemove())
            await state.finish()
