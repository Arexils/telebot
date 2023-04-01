import asyncio
import random

from aiogram import types

from loader import dp


@dp.message_handler(
    content_types=types.ContentType.PHOTO,
)
async def echo_photo(msg: types.Message):
    photo = msg.photo[-1]
    caption = (
        f"<b>Размер:</b> <code>{photo.file_size}</code> kByte\n"
        f"<b>Ширина:</b> <code>{photo.width}</code> px\n"
        f"<b>Высота:</b> <code>{photo.height}</code> px\n"
    )
    await msg.answer('Сейчас обработаю фото!')
    await asyncio.sleep(random.randint(1, 7))
    await msg.answer_photo(
        photo.file_id,
        caption=msg.caption if msg.caption else caption,
    )
