from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("auth", "Ввести код авторизации"),
            types.BotCommand("books", "Найти книгу"),
            types.BotCommand("balance", "Показать баланс и ссылку")
        ]
    )
