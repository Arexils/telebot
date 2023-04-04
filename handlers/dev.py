import logging

from aiogram import types

from loader import dp


@dp.message_handler(commands=['dev', ])
async def command_start(msg: types.Message):
    ar = msg.get_args().split()
    logging.info(ar)
    # non_existing_user = 111111
    # # не попадает в error handler, так как обрабатывается try..except
    # try:
    #     await msg.answer("Неправильно закрыт <b>тег<b>")
    # except Exception as err:
    #     await msg.answer(f'Не попало в error handler. Ошибка {err}')
    #
    # # не попадает в error handler, так как обрабатывается try..except
    # try:
    #     await bot.send_message(chat_id=non_existing_user, text='Несуществующий пользователь')
    # except Exception as err:
    #     await msg.answer(f'Не попало в error handler. Ошибка {err}')
    #
    # # попадает в error handler
    # await msg.answer('Не сущетствует <fff>тега</fff>')
    # logging.info('Это не выполнится, но бот не упадет')
    #
    # # все что ниже не выполнится
    # await msg.answer('hello')
    # await msg.answer('щас <32hone>все упадет!!!!"№№</32hone>!')

    try:
        await msg.answer(f'{ar[0]}')
    except IndexError as e:
        logging.info(f'это try: {e}')
