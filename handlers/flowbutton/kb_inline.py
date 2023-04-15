from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp
from utils.keyborads.dev_inline import kb_inline, inline_kb_full


@dp.message_handler(commands=['kb_inline', ])
async def command_start(msg: types.Message):
    await msg.answer('кнопкиииии', reply_markup=kb_inline)


@dp.message_handler(commands=['kb_inline_full', ])
async def command_start(msg: types.Message):
    await msg.answer('кнопкиииии', reply_markup=inline_kb_full)


@dp.callback_query_handler(text='button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await callback_query.answer('wow')
    await callback_query.message.answer('Нажата первая кнопка!')


@dp.callback_query_handler(Text(startswith='btn'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    if code.isdigit():
        code = int(code)
    if code == 2:
        await callback_query.answer('Нажата вторая кнопка')
    elif code == 5:
        await callback_query.answer(
            text=(
                'Нажата кнопка с номером 5.\n'
                'А этот текст может быть длиной до 200 символов'
            ),
            show_alert=True)
    else:
        await callback_query.answer(callback_query.id)
    await callback_query.answer(f'Нажата инлайн кнопка! code={code}')
