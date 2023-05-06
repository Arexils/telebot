from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ContentType
from aiogram.utils.callback_data import CallbackData

from handlers.moderate.group import channels
from loader import dp


class NewPost(StatesGroup):
    EnterMessage = State()
    Confirm = State()


@dp.message_handler(commands='create_post')
async def create_post(msg: Message, state: FSMContext):
    await msg.answer("Отправьте мне пост для публикации")
    await state.set_state(NewPost.EnterMessage.state)


post_callback = CallbackData('create_post', 'action')
confirmation_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Опубликовать пост', callback_data=post_callback.new(action='post')),
            InlineKeyboardButton(text='Отклонить', callback_data=post_callback.new(action='cancel')),
        ]
    ]
)


@dp.message_handler(state=NewPost.EnterMessage)
async def enter_message(msg: Message, state: FSMContext):
    await state.update_data(text=msg.html_text, mention=msg.from_user.get_mention())
    await msg.answer('Вы собираетесь отправить пост на проверку?', reply_markup=confirmation_keyboard)
    await state.set_state(NewPost.Confirm.state)


@dp.callback_query_handler(post_callback.filter(action='post'), state=NewPost.Confirm)
async def confirm_post(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("text")
    mention = data.get("mention")
    await state.finish()
    await callback.message.delete_reply_markup()
    await callback.message.answer("Вы отправили текст на проверку")

    # await bot.send_message(chat_id='id админа', f'Пользователь {mention} хочет сделать пост:')
    # await bot.send_message(chat_id='id админа', text=text, parse_mode="HTML", reply_markup=confirmation_keyboard)

    await callback.message.answer(text=f'Пользователь {mention} хочет сделать пост:\n\n{text}', parse_mode="HTML", reply_markup=confirmation_keyboard)


@dp.callback_query_handler(post_callback.filter(action='cancel'), state=NewPost.Confirm)
async def cancel_post(callback: CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.edit_reply_markup()
    await callback.message.answer('Вы отклонили пост')


@dp.message_handler(state=NewPost.Confirm)
async def _post_unknown(msg: Message):
    await msg.answer('Выберите опубликовать или отклонить текст')


@dp.callback_query_handler(post_callback.filter(action='post'), )
async def approve_post(call: CallbackQuery):
    await call.answer('Вы одобрили этот пост', show_alert=True)
    target_channel = channels[0]
    message = await call.message.edit_reply_markup()
    await message.send_copy(chat_id=target_channel)


@dp.callback_query_handler(post_callback.filter(action='cancel'), )
async def decline_post(call: CallbackQuery):
    await call.answer('Вы отклонили этот пост', show_alert=True)
    await call.message.edit_reply_markup()


@dp.message_handler()
async def catch_text(msg: Message):
    await msg.answer('Вы прислали текст')


@dp.message_handler(content_types=ContentType.DOCUMENT)
async def catch_text(msg: Message):
    await msg.document.download()
    await msg.reply(
        'Документ скачан\n'
        f'<pre>FILE ID = {msg.document.file_id}</pre>',
    )


@dp.message_handler(content_types=ContentType.AUDIO)
async def catch_text(msg: Message):
    await msg.audio.download()
    await msg.reply(
        'Аудио скачано\n'
        f'<pre>FILE ID = {msg.audio.file_id}</pre>',
    )


@dp.message_handler(content_types=ContentType.VIDEO)
async def catch_text(msg: Message):
    await msg.video.download()
    await msg.reply(
        'Видео скачано\n'
        f'<pre>FILE ID = {msg.video.file_id}</pre>',
    )


@dp.message_handler(content_types=ContentType.PHOTO)
async def catch_text(msg: Message):
    await msg.photo[-1].download()
    await msg.reply(
        'Аудио скачано\n'
        f'<pre>FILE ID = {msg.photo[-1].file_id}</pre>',
    )


@dp.message_handler(content_types=ContentType.ANY)
async def catch_text(msg: Message):
    await msg.reply(f'Вы прислали  {msg.content_type}')
