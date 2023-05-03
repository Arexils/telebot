from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from handlers.flowbutton.shop.filters.filters import IsUser
from handlers.flowbutton.shop.user.menu import balance
from loader import dp


@dp.callback_query_handler(IsUser(), text=balance.callback_data)
async def process_balance(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Ваш кошелек пуст! Чтобы его пополнить нужно...')
    await callback.message.answer('Ваш кошелек пуст! Чтобы его пополнить нужно...')
