from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.storage import FSMContext

from loader import dp, db
from states import Inp_link


@dp.message_handler(text='/auth')
async def auth(message: types.Message):
    if await db.get_user(message.from_user.id):
        await message.answer('Вы уже авторизованны!')
    else:
        mess = await message.answer('Чтобы авторизоваться введите код \nКод: pIlPSsf2Er', 
                            reply_markup=InlineKeyboardMarkup(
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(
                                            text='отменить',
                                            callback_data='back'
                                        )
                                    ],
                                ]))

        await Inp_link.Code.set()
        await state.update_data(mess=mess)

@dp.message_handler(state=Inp_link.Code)
async def auth_inp_code(message: types.Message, state: FSMContext):
    user_ref_data = await db.check_ref_link(message.text)
    data = await state.get_data()
    prev_mess = data.get('mess')

    if user_ref_data:
        user_ref_id = user_ref_data['id']
        user_ref_balance = user_ref_data['balance']
        await db.add_user(message.from_user.id)
        await db.ref_point(user_ref_id, user_ref_balance)

        await message.answer('Теперь ты можешь пользоваться ботом')

        await state.finish()
        await prev_mess.edit_reply_markup()
    else:
        await message.answer('Код неверный!')
