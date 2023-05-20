import logging

from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import Update
from aiogram.utils import exceptions

from loader import dp


@dp.errors_handler()
async def errors_handler(update: Update, exception: exceptions):
    if isinstance(exception, exceptions.CantDemoteChatCreator):
        logging.error("Can't demote chat creator")
        return True

    if isinstance(exception, exceptions.MessageNotModified):
        logging.error('Message is not modified')
        return True
    if isinstance(exception, exceptions.MessageCantBeDeleted):
        logging.error('Message cant be deleted')
        return True

    if isinstance(exception, exceptions.MessageToDeleteNotFound):
        logging.error('Message to delete not found')
        return True

    if isinstance(exception, exceptions.MessageTextIsEmpty):
        await update.message.answer('Не верные аргументы')
        logging.error('MessageTextIsEmpty - получили пустоту')
        # return True
        return True

    if isinstance(exception, exceptions.Unauthorized):
        logging.info(f'Unauthorized: {exception}')
        return True

    if isinstance(exception, exceptions.InvalidQueryID):
        logging.exception(f'InvalidQueryID: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, exceptions.CantParseEntities):
        logging.exception(f'CantParseEntities: {exception} \nUpdate: {update}')
        await update.message.answer(f'Попало в error handler. CantParseEntities: {exception.args}')
        return True

    if isinstance(exception, exceptions.RetryAfter):
        logging.exception(f'RetryAfter: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, exceptions.BadRequest):
        logging.exception(f'CantParseEntities: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, CancelHandler):
        logging.exception(f' edf')
        return True
    logging.exception(f'Update: {update} \n{exception}')
