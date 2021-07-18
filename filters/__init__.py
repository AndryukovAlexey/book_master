from re import A
from aiogram import Dispatcher

from loader import dp
from .availability import AvailabilityInDbMess, AvailabilityCall
from .via import Via_bot


if __name__ == "filters":
    dp.filters_factory.bind(AvailabilityInDbMess)
    dp.filters_factory.bind(AvailabilityCall)
    dp.filters_factory.bind(Via_bot)

    
