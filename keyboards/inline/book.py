from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.deep_linking import get_start_link


buy_book = CallbackData('buy', 'book_id', 'book_name', 'book_price')

async def inline_buy_book(book_id, book_name, book_price):
    keybord = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text='купить книгу',
                                callback_data=buy_book.new(
                                    book_id=book_id,
                                    book_name=book_name,
                                    book_price=book_price)
                            )
                        ],
                    ])
    
    return keybord

async def inline_show_book(book_id):
    keybord = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text='показать товар',
                                url= await get_start_link(str(book_id))
                                
                            )
                        ],
                    ])
    
    return keybord

