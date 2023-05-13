from aiogram.types import Message, ShippingQuery, PreCheckoutQuery

from handlers.flow_payments import NoteBook, POST_FAST_SHIPPING, POST_REGULAR_SHIPPING, PICKUP_SHIPPING
from loader import dp


@dp.message_handler(commands='invoices')
async def show_invoices(msg: Message):
    await msg.bot.send_invoice(msg.from_user.id, **NoteBook.generate_invoices(), payload='12345')


@dp.shipping_query_handler()
async def choose_shipping(shipping_query: ShippingQuery):
    if shipping_query.shipping_address.country_code == 'RU':
        await shipping_query.bot.answer_shipping_query(
            shipping_query_id=shipping_query.id,
            shipping_options=[
                POST_REGULAR_SHIPPING,
                POST_FAST_SHIPPING,
                PICKUP_SHIPPING,
            ],
            ok=True,
        )
    elif shipping_query.shipping_address.country_code == 'US':
        await shipping_query.bot.answer_shipping_query(
            shipping_query_id=shipping_query.id,
            ok=False,
            error_message='Сюда не доставляем'
        )
    else:
        await shipping_query.bot.answer_shipping_query(
            shipping_query_id=shipping_query.id,
            shipping_options=[POST_REGULAR_SHIPPING],
            ok=True
        )


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id, ok=True)
    await pre_checkout_query.bot.send_message(chat_id=pre_checkout_query.from_user.id, text='Спасибо за покупку')
