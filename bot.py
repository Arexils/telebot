import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils.exceptions import BotBlocked

from config import TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.errors_handler(exception=BotBlocked)
async def blocked_bot(update: types.Update, exception: BotBlocked):
    print(f'Меня заблокировали. msg: {update}, exception: {exception}')
    return True


@dp.message_handler(commands=['start'])
async def command_start(msg: types.Message):
    await msg.reply('reply')
    await msg.answer('answer')
    await bot.send_message(chat_id=msg.from_user.id, text='send_message')


@dp.message_handler(commands=['help'])
async def command_test(msg: types.Message):
    await msg.reply('я не могу что-то подсказать')


@dp.message_handler(commands=['dice'])
async def dice(msg: types.Message):
    await msg.answer_dice(emoji='🎲', )


@dp.message_handler()
async def echo_bot(msg: types.Message):
    await asyncio.sleep(7)
    await msg.answer(f'Это это ответ вам: {msg.text}')


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
