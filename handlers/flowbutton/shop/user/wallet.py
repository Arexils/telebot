from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from handlers.flowbutton.shop.filters.filters import IsUser
from handlers.flowbutton.shop.user.menu import balance
from loader import dp


@dp.message_handler(IsUser(), text=balance)
async def process_balance(msg: Message, state: FSMContext):
    await msg.answer('Ваш кошелек пуст! Чтобы его пополнить нужно...')
