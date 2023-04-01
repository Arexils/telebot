from aiogram import types

from loader import dp


@dp.message_handler(
    content_types=types.ContentType.TEXT,
)
async def echo_msg(msg: types.Message, ):
    await msg.answer(f'Echo: {msg.text}')
