from dataclasses import dataclass
from typing import List

from aiogram.types import LabeledPrice

import config


@dataclass
class Item:
    title: str
    description: str
    start_parameter: str
    currency: str
    prices: List[LabeledPrice]
    provider_data: dict = None
    photo_url: str = None
    photo_size: int = None
    photo_width: int = None
    photo_height: int = None
    need_name: bool = False
    need_phone_number: bool = False
    need_email: bool = False
    need_shipping_address: bool = False
    send_phone_number_to_provider: bool = False
    send_email_to_provider: bool = False
    is_flexible: bool = False
    provider_token: str = config.PROVIDER_PAYMASTER_TOKEN

    def generate_invoices(self):
        return self.__dict__


NoteBook = Item(
    title='Ноутбук Lenovo IP Gaming 3',
    description=(
        'Выведите игровой процесс киберспортивных дисциплин на новый уровень с помощью устройства, '
        'которое поможет опередить конкурентов и занять первые строчки в списках лидеров'
    ),
    currency='RUB',
    prices=[
        LabeledPrice(
            label='Ноутбук Lenovo IP Gaming 3',
            amount=30_000_00
        ),
        LabeledPrice(
            label='Доставка',
            amount=500_00
        ),
        LabeledPrice(
            label='Скидка',
            amount=-2_000_00
        )

    ],
    start_parameter='create_invoice_lenovo_3',
    photo_url="https://items.s1.citilink.ru/1595005_v01_b.jpg",
    photo_size=600,
    need_shipping_address=True,
    is_flexible=True

)
