from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class Via_bot(BoundFilter):

    async def check(self, message: types.Message):

        return message['via_bot'] == None