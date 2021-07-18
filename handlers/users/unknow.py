from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types.message import ContentType

from loader import dp, db
from filters import Via_bot

@dp.callback_query_handler(text='back', state='*')
async def cancel_state(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()

    await state.finish()

@dp.message_handler(Via_bot(), state=None)
async def bot_unknow(message: types.Message):
    if await db.get_user(message.from_user.id):
        await message.answer('Такой команды нет \nдля вывода списка всех команд введите: /help')
    else:
        await message.answer('Вы не авторизированны! \nДля авторизации пройдите по реферальной ссылке'
                                'или введите код вручную по команде /auth')

