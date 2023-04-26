from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove

from loader import dp

# Эти значения далее будут подставляться в итоговый текст, отсюда
# такая на первый взгляд странная форма прилагательных
available_food_names = ['суши', 'спагетти', 'хачапури']
available_food_sizes = ['маленькую', 'среднюю', 'большую']


class OrderFood(StatesGroup):
    waiting_for_food_name = State()
    waiting_for_food_size = State()


@dp.message_handler(commands='food', state='*')
async def food_start(msg: Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_food_names:
        keyboard.add(name)
    await msg.answer('Выберите блюдо:', reply_markup=keyboard)
    # await OrderFood.waiting_for_food_name.set()  # <-- Плохой вариант записи
    await state.set_state(OrderFood.waiting_for_food_name.state)


@dp.message_handler(commands='cancel', state='*')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cmd_cancel(msg: Message, state: FSMContext):
    await state.finish()
    await msg.answer('Действие отменено', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=OrderFood.waiting_for_food_name)
async def food_chosen(msg: Message, state: FSMContext):
    if msg.text.lower() not in available_food_names:
        await msg.answer('Пожалуйста, выберите блюдо, используя клавиатуру ниже.')
        return
    await state.update_data(chosen_food=msg.text.lower())

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for size in available_food_sizes:
        keyboard.add(size)
    await state.set_state(OrderFood.waiting_for_food_size.state)
    await msg.answer('Теперь выберите размер порции:', reply_markup=keyboard)


@dp.message_handler(state=OrderFood.waiting_for_food_size)
async def food_size_chosen(msg: Message, state: FSMContext):
    if msg.text.lower() not in available_food_sizes:
        await msg.answer('Пожалуйста, выберите размер порции, используя клавиатуру ниже.')
        return
    user_data = await state.get_data()
    await msg.answer(
        f'Вы заказали {msg.text.lower()} порцию {user_data["chosen_food"]}.',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.finish()
    # await state.reset_state(with_data=False)  # Сбросит только состояние, а данные сохранятся
