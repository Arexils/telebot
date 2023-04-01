from aiogram import types
from aiogram.dispatcher.filters import IDFilter
from aiogram.utils import markdown

import config
from loader import dp


@dp.message_handler(commands=['info'])
async def command_info_profile(msg: types.Message):
    text = (
        f'{msg.from_user.mention}\n'
        f'<b>ID: </b> <code>{msg.from_user.id}</code>\n'
        f'<b>Chat ID: </b> {msg.chat.id}\n'
    )
    await msg.answer(text)


#
@dp.message_handler(IDFilter(config.ADMINS), commands=['info_2'])
async def command_info_profile_2(msg: types.Message):
    text = markdown.text(
        msg.from_user.mention,
        markdown.text(
            markdown.bold('ID: '),
            markdown.code(msg.from_user.id),
        ),
        markdown.text(
            markdown.bold('Chat ID: '),
            msg.chat.id,
        ),
        sep='\n'
    )
    await msg.answer(text, parse_mode=types.ParseMode.MARKDOWN_V2)
