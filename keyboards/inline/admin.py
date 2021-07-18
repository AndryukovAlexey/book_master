from states.admin import Choice_book
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


delete_book = CallbackData('delete', 'book_id')
edit_book = CallbackData('edit', 'book_id')

async def del_or_edit(book_id):
    keybord = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text='Удалить',
                                callback_data=delete_book.new(
                                    book_id=book_id
                                )
                                
                            ),
                            InlineKeyboardButton(
                                text='Изменить',
                                callback_data=edit_book.new(
                                    book_id=book_id
                                )
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                text='Отменить',
                                callback_data='back'
                            )
                        ]
                    ])
    
    return keybord


async def menu_edit():
    keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text='Название',
                                callback_data='edit_name'
                                
                            ),
                            InlineKeyboardButton(
                                text='цена',
                                callback_data='edit_price'
                            ),
                            InlineKeyboardButton(
                                text='фото',
                                callback_data='edit_photo'
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                text='Изменить',
                                callback_data='save_changes'
                            )
                        ]
                    ])
    
    return keyboard