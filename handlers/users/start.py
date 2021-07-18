from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import user

from loader import dp, db
from filters import AvailabilityInDbMess

from re import compile


@dp.message_handler(CommandStart(deep_link=compile(r'.{3,10}')))
async def reg_user(message: types.Message):
    user_ref_data = await db.check_ref_link(message.get_args())
    
    if await db.get_user(message.from_user.id):
        await message.answer('Вы уже авторизованны, либо ссылка неверна!')
    else:
        if user_ref_data:
            user_ref_id = user_ref_data['id']
            user_ref_balance = user_ref_data['balance']
            await db.add_user(message.from_user.id)
            await db.ref_point(user_ref_id, user_ref_balance)

            await message.answer('Теперь ты можешь пользоваться ботом!')
        else:
            await message.answer('Ссылка неверна')



@dp.message_handler(AvailabilityInDbMess(), CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")
