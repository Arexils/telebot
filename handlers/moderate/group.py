import asyncio
import datetime
import re

from aiogram import types
from aiogram.dispatcher.filters import AdminFilter, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import BadRequest

from handlers.moderate.filters.manage_filters import IsGroup, IsChannel
from loader import dp


@dp.message_handler(IsGroup(), Command('ro', prefixes='!/'), AdminFilter())
async def read_only_mode(msg: types.Message):
    member = msg.reply_to_message.from_user
    command_parse = re.compile(r'(!ro|/ro) ?(\d+)? ?([a-zA-Z ])+?')
    parsed = command_parse.match(msg.text)
    time = parsed.group(2)
    comment = parsed.group(3)
    if not time:
        time = 5
    else:
        time = int(time)
    until_date = datetime.datetime.now() + datetime.timedelta(minutes=time)
    ReadOnlyPermission = types.ChatPermissions(
        can_send_messages=False,
        can_send_media_messages=False,
        can_send_polls=False,
        can_pin_messages=False,
        can_invite_users=True,
        can_change_info=False,
        can_add_web_page_previews=False,
    )
    try:
        await msg.bot.restrict_chat_member(
            msg.chat.id,
            user_id=member.id,
            permissions=ReadOnlyPermission,
            until_date=until_date
        )
        await msg.answer(
            f'Пользователю {member.get_mention(as_html=True)} запрещено писать на {time} минут по причине {comment}')
    except BadRequest:

        await msg.answer('Пользователь является администратором')
        service_message = await msg.reply('Сообщение удалится через 5 секунд')
        await asyncio.sleep(5)
        await msg.delete()
        await service_message.delete()


@dp.message_handler(IsChannel(), content_types=types.ContentType.ANY)
async def get_channel_info(message: types.Message):
    await message.answer(
        f'Сообщение прислано с канала {message.forward_from_chat.title}. \n'
        f'Username: @{message.forward_from_chat.username}. \n'
        f'ID: {message.forward_from_chat.id}'
    )


check_button = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='Проверить подписки', callback_data="check_subs"),
)

channels = (-1001843483497,)  # Список каналов


@dp.message_handler(Command("channels"))
async def show_channels(msg: types.Message):
    channels_format = ''
    for channel in channels:
        channels_format = str()
        chat = await msg.bot.get_chat(channel)
        invite_link = await chat.export_invite_link()
        channels_format += f'Канал <a href="{invite_link}">{chat.title}</a>\n\n'
    await msg.answer(
        f'Вам необходимо подписаться на следующие каналы: \n'
        f'{channels_format}',
        reply_markup=check_button,
        disable_web_page_preview=True
    )


async def check(bot, user_id, channel: int | str):
    # bot = Bot.get_current()
    member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
    return member.is_chat_member()


@dp.callback_query_handler(text='check_subs')
async def checker(callback: types.CallbackQuery):
    result = str()
    for channel in channels:
        status = await check(bot=callback.bot, user_id=callback.from_user.id, channel=channel)
        channel = await callback.message.bot.get_chat(channel)
        if status:
            result += f'Подписка на канал {channel.title} оформлена!'
        else:
            invite_link = await channel.export_invite_link()
            result += (f'Подписка на канал {channel.title} не оформлена!'
                       f'<a href="{invite_link}">Нужно  подписаться.</a>\n\n')
    await callback.message.edit_text(f'{result}', disable_web_page_preview=False, reply_markup=check_button)
    await callback.answer('ready!')
