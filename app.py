from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from loader import db


async def on_startup(dispatcher):
    
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # подключаю фильтры/мидлвари

    #создаю таблицы
    await db.create_tables()
    
    #создаю юзера, для получения реф ссылки
    await db.add_user(123)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    
    executor.start_polling(dp, on_startup=on_startup)
