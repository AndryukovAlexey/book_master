from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

async def back(text):
    keybord = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text=text,
                                callback_data='back'
                                
                            )
                        ],
                    ])
    
    return keybord
