from aiogram import types
from aiogram.utils.deep_linking import get_start_link

from loader import dp, db


@dp.message_handler(commands=['balance'])
async def profile(message: types.Message):
    user = await db.get_user(message.from_user.id)
    balance = user['balance']
    ref_code = user['ref_link']
    ref_link = await get_start_link(ref_code)

    await message.answer(f"Ваш баланс: {balance}руб \nВаша реферальная ссылка: {ref_link}\n"
                        "За каждого реферала вам зачисляется 100руб!")
    
