from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp

@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Бот покупки книг.",
            "У бота есть функция авторизации по реферальной ссылке, либо ввода кода вручну",
            "Авторизовавшимся доступны поиск и покупка книг",
            "У бота есть админ-панель, а также django админка",
            "Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку",
            "/auth - Ввести код авторизации",
            "/books - поиск и выбор интересующей вас книги")
    
    await message.answer("\n".join(text))
