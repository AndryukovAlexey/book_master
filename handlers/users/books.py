from aiogram.dispatcher.storage import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from aiogram.dispatcher.filters import CommandStart, Command, state

from loader import dp, db, bot
from filters import AvailabilityCall
from keyboards.inline import buy_book, inline_buy_book
from utils.misc import create_invoice, SHIPPING
from states import Quantity_books

from re import compile


@dp.message_handler(AvailabilityCall(), CommandStart(deep_link=compile(r'\d{1,3}')))
async def show_item(message: types.Message, state: FSMContext):
    book_id = int(message.get_args())
    book = await db.get_book(book_id)
    if book:
        book_name = book['name']
        book_photo = book['photo']
        book_price = book['price']

        await state.update_data(book_photo=book_photo)

        await message.answer_photo(photo=book_photo,
                                    caption=f"книга: {book_name} \nцена: {book_price}",
                                    reply_markup= await inline_buy_book(book_id, book_name, book_price))
    else:
        await message.answer('Такой книги у нас нет!')

@dp.callback_query_handler(buy_book.filter(), state="*")
async def quant_books(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    book_id = int(callback_data.get('book_id'))
    book_name = callback_data.get('book_name')
    book_price = int(callback_data.get('book_price'))

    await call.message.answer('Введите количество книг', reply_markup=InlineKeyboardMarkup(
                                                            inline_keyboard=[
                                                                [
                                                                    InlineKeyboardButton(
                                                                        text='отменить',
                                                                        callback_data='back'
                                                                    )
                                                                ],
                                                            ]))

    await Quantity_books.Quant.set()
    await state.update_data(book_id=book_id, book_name=book_name, book_price=book_price)               

@dp.message_handler(state=Quantity_books.Quant)
async def buy_item(message: types.Message, state: FSMContext):
    data = await state.get_data()
    book_id = int(data.get('book_id'))
    book_name = data.get('book_name')
    book_photo = data.get('book_photo')
    book_price = int(str(data.get('book_price')) + "00")
    try:
        book_quant = int(message.text)
    except ValueError:
        await message.answer('Введите кол-во числом!')
        return
    
    balance = await db.get_balance(message.from_user.id)
    balance = int(str(balance['balance'])+'00')
    
    await state.finish()

    book = await create_invoice(book_id, book_name, book_price, book_photo, book_quant, balance)

    await bot.send_invoice(message.from_user.id,
                            **book,
                            payload=book_id)
    
@dp.shipping_query_handler()
async def choose_shipping(query: types.ShippingQuery):
    
    await bot.answer_shipping_query(shipping_query_id=query.id,
                                    shipping_options=[SHIPPING],
                                    ok=True)

@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=query.id,
                                        ok=True)

    await bot.send_message(chat_id=query.from_user.id,
                            text='Спасибо за покупку! Уже отправляем')

