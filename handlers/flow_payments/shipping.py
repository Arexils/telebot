from aiogram.types import ShippingOption, LabeledPrice

POST_REGULAR_SHIPPING = ShippingOption(
    id='post_reg',
    title='Почтой',
    prices=[
        LabeledPrice(
            'Обычная коробка', 0
        ),
        LabeledPrice(
            'Почтой', 500_00
        ),
    ]
)

POST_FAST_SHIPPING = ShippingOption(
    id='post_fast',
    title='Почтой ускоренная',
    prices=[
        LabeledPrice(
            'Прочная упаковка', 200_00
        ),
        LabeledPrice(
            'Срочной почтой', 1000_00
        ),
    ]
)

PICKUP_SHIPPING = ShippingOption(
    id='pickup',
    title='Самовывоз',
    prices=[
        LabeledPrice(
            'Самовывоз из магазина', -100_00
        ),
    ]
)
