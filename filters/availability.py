from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from loader import db
from data.config import ADMINS

class AvailabilityCall(BoundFilter):

    async def check(self, callback: types.CallbackQuery):
        if str(callback.from_user.id) in ADMINS:
            return True
        else:
            user = await db.get_user(callback.from_user.id)
            return user != None


class AvailabilityInDbMess(BoundFilter):

    async def check(self, message: types.Message):
        if str(message.from_user.id) in ADMINS:
            return True
        else:
            user = await db.get_user(message.from_user.id)
            return user != None

