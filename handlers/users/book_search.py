from aiogram import types
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

from loader import dp
from filters import AvailabilityInDbMess


@dp.message_handler(AvailabilityInDbMess(), commands=['books'])
async def search_mode(message: types.Message):
    await message.answer('Для выбора книги нажмите на кнопку ниже и введите название книги',
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=[
                                [
                                    InlineKeyboardButton(
                                        text='найти книгу',
                                        switch_inline_query_current_chat=''
                                        
                                    )
                                ],
                            ]))

