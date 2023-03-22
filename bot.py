import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from config import TOKEN
from utils import knd_logic, RPS

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.INFO)


class Form(StatesGroup):
    name = State()


async def on_startup(dp):
    logging.info('new start')


async def on_shotdown(dp):
    logging.info('end start')


@dp.message_handler(commands=['knb'])
async def knb(message: types.Message):
    """Conversation entrypoint"""

    # Set state
    await Form.name.set()
    await message.reply(
        (
            f'Введите предмет для игры к КНБ\n'
            f'[{", ".join(RPS)}]: '
        )
    )


# You can use state='*' if you want to handle all states
@dp.message_handler(state='*', commands=['cancel'])
async def cancel_handler(message: types.Message, state: FSMContext):
    """Allow user to cancel action via /cancel command"""

    current_state = await state.get_state()
    if current_state is None:
        # User is not in any state, ignoring
        return

    # Cancel state and inform user about it
    await state.finish()
    await message.reply('Cancelled.')


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    """Process user name"""

    # Finish our conversation
    await state.finish()
    result, bot_selection = knd_logic(message.text)
    await message.reply(f'Бот выбрал: {bot_selection}.\nПобедитель: {result}')  # <-- Here we get the name


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shotdown,
    )
