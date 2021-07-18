from aiogram import types
from aiogram.types import labeled_price
from aiogram.types.labeled_price import LabeledPrice


from utils.misc import Item


async def create_invoice(book_id, book_name, book_price, book_photo, book_quant, balance):
    book = Item(
        title=book_name + f' {book_quant}шт',
        description=book_name + f' {book_quant}шт. \nДля покупки используйте тест-карту: 1111 1111 1111 1026, 12/22, CVC 000. \nПокупки на суммы больше 1тр недоступны!',
        currency="RUB",
        prices=[
            LabeledPrice(
                label=book_name + f' {book_quant}шт',
                amount=book_price * book_quant
            ),
            LabeledPrice(
                label='Ваш баланс',
                amount=-balance
            )
        ],
        start_parameter=book_id,
        photo_url=book_photo,
        need_shipping_address=True
    )

    return book.generate_invoice()

SHIPPING = types.ShippingOption(
    id='shipp',
    title='херовая доставка',
    prices=[
        LabeledPrice(
            'Почта России', 10000
        )
    ]
)
