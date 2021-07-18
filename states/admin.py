from aiogram.dispatcher.filters.state import StatesGroup, State


class Add_book(StatesGroup):
    Name = State()
    Price = State()
    Photo = State()
    Confirm = State()

class Choice_book(StatesGroup):
    Id = State()

class Edit_book(StatesGroup):
    Choice = State()
    Name = State()
    Price = State()
    Photo = State()
    
