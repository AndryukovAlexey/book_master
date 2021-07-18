import logging
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, message
from aiogram import types

from data.config import ADMINS
from loader import dp, db
from states import Add_book, Choice_book, Edit_book
from keyboards.inline import back, del_or_edit, delete_book, edit_book, menu_edit


@dp.message_handler(commands=['admin_panel'], user_id=ADMINS)
async def admin_panel(message: types.Message):
    await message.answer('Какое действие вы хотите совершить с товарами?',
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=[
                                [
                                    InlineKeyboardButton(
                                        text='Добавить',
                                        callback_data='add'
                                        
                                    )
                                ],
                                [
                                    InlineKeyboardButton(
                                        text='Удалить/Изменить',
                                        callback_data='del/edit'
                                    )
                                ]
                            ]))




# ДОБАВЛЕНИЕ ТОВАРА!!

@dp.callback_query_handler(text='add')
async def add_book(call: types.CallbackQuery, state: FSMContext):
    mess = await call.message.edit_text('Введите название книги', reply_markup=await back('отменить'))

    await Add_book.Name.set()
    await state.update_data(mess=mess)

@dp.message_handler(state=Add_book.Name)
async def add_book_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    # так я удаляю у предыдущего сообщения инлайн кнопку
    pre_mess = data.get('mess')
    await pre_mess.edit_reply_markup()

    book_name = message.text

    mess = await message.answer('Введите цену книги', reply_markup=await back('Вернуться к названию'))

    await state.update_data(book_name=book_name, mess=mess)
    await Add_book.Price.set() 

@dp.message_handler(state=Add_book.Price)
async def add_book_price(message: types.Message, state: FSMContext):
    try:
        book_price = int(message.text)
    except ValueError:
        await message.answer('Введите цену числом!')
        return

    data = await state.get_data()
    pre_mess = data.get('mess')
    await pre_mess.edit_reply_markup()

    mess = await message.answer('Отправьте url ссылку на фото(размером 780x780)',
                                reply_markup=await back('вернуться к цене'))

    await state.update_data(book_price=book_price, mess=mess) 
    await Add_book.Photo.set()

@dp.message_handler(state=Add_book.Photo, content_types=['photo', 'text'])
async def add_book_photo(message: types.Message, state: FSMContext):

    if message.photo:
        await message.answer('отправьте URL ССЫЛКУ!')
        return
    
    book_photo = message.text
    if 'http' not in book_photo:
        await message.answer('Ссылка не валидна!')
        return
        
    data = await state.get_data()
    pre_mess = data.get('mess')

    await pre_mess.edit_reply_markup()
       
    await state.update_data(book_photo=book_photo)
    await Add_book.Confirm.set()

    
    book_name = data.get('book_name')
    book_price = data.get('book_price')

    await message.answer_photo(photo=book_photo,
                                caption=f"книга: {book_name} \nцена: {book_price}",
                                reply_markup=InlineKeyboardMarkup(
                                                    inline_keyboard=[
                                                        [
                                                            InlineKeyboardButton(
                                                                text='Подтвердить и добавить',
                                                                callback_data='confirm_add'
                                                                
                                                            )
                                                        ],
                                                        [
                                                            InlineKeyboardButton(
                                                                text='Отменить',
                                                                callback_data='back'
                                                            )
                                                        ]
                                                    ]))

@dp.callback_query_handler(text='confirm_add', state=Add_book.Confirm)
async def conf_add_book(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    book_name = data.get('book_name')
    book_price = data.get('book_price')
    book_photo = data.get('book_photo')

    await db.add_book(book_name, book_price, book_photo)

    await call.message.edit_reply_markup()
    await call.message.answer('Книга успешно добавленна!')

    await state.finish()

@dp.callback_query_handler(text='back', state=Add_book.Price)
async def back_to_name(call: types.CallbackQuery, state: FSMContext):
    await Add_book.previous()

    await call.message.edit_text('Введите название книги', reply_markup=await back('отменить'))

@dp.callback_query_handler(text='back', state=Add_book.Photo)
async def back_to_price(call: types.CallbackQuery, state: FSMContext):
    await Add_book.previous()

    await call.message.edit_text('Введите цену книги', reply_markup=await back('Вернуться к названию'))







# УДАЛЕНИЕ/ИЗМЕНЕНИЕ ТОВАРА

@dp.callback_query_handler(text='del/edit')
async def show_books(call: types.CallbackQuery, state: FSMContext):
    all_books = await db.get_all_books()
    books = []

    for book in all_books:
        book_id = book['id']
        book_name = book['name']
        book_price = book['price']
        
        books.append(f"id - {book_id}, название - {book_name}, цена - {book_price}\n")

    books.append('\nДля выбора действия - введите id книги')

    mess = await call.message.edit_text(''.join(mess for mess in books), reply_markup= await back('Отменить'))

    await Choice_book.Id.set()
    await state.update_data(mess=mess)

@dp.message_handler(state=Choice_book.Id)
async def choice_book(message: types.Message, state: FSMContext):
    try:
        book_id = int(message.text)
    except ValueError:
        await message.answer('Введите id числом!')
        return
    
    book = await db.get_book(book_id)

    if book:
        book_name = book['name']
        book_price = book['price']
        book_photo = book['photo']

        data = await state.get_data()
        pre_mess = data.get('mess')

        await pre_mess.edit_reply_markup()
        
        mess = await message.answer_photo(photo=book_photo,
                                    caption=f"Название: {book_name} \nцена: {book_price}",
                                    reply_markup=await del_or_edit(book_id))
    else:
        await message.answer('Книги с таким id не найдено!')
        return
    
    await state.update_data(mess=mess)




# УДАЛЕНИЕ КНИГИ

@dp.callback_query_handler(delete_book.filter(), state="*")
async def delete_book(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    book_id = int(callback_data.get('book_id'))

    await db.delete_book(book_id)

    await call.message.edit_reply_markup()

    await call.message.answer('Книга успешно удаленна!')

    await state.finish()




# РЕДАКТИРОВАНИЕ КНИГИ

@dp.callback_query_handler(edit_book.filter(), state="*")
async def edit_book(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()

    book_id = int(callback_data.get('book_id'))
    mess = await call.message.edit_reply_markup(reply_markup=await menu_edit())

    await Edit_book.Choice.set()
    await state.update_data(book_id=book_id, menu_mess=mess)

# Изменяю название
@dp.callback_query_handler(text=['edit_name', 'edit_price', 'edit_photo'], state=Edit_book.Choice)
async def choice_edit_param(call: types.CallbackQuery, state: FSMContext):
    text = call.data

    if text == 'edit_name':
        mess = await call.message.answer('Введите новое название', reply_markup=await back('назад'))
        await Edit_book.Name.set()
    if text == 'edit_price':
        mess = await call.message.answer('Введите новую цену', reply_markup=await back('назад'))
        await Edit_book.Price.set()
    if text == 'edit_photo':
        mess = await call.message.answer('Введите url ссылку на новое изображение',
                                        reply_markup=await back('назад'))
        await Edit_book.Photo.set()

    await call.message.edit_reply_markup()
    await state.update_data(prev_mess=mess) 

# получаю изменения
@dp.message_handler(state=Edit_book)
async def edit_name_book(message: types.Message, state: FSMContext):
    current_state = str(await state.get_state()).split(':')[-1]
    print(current_state)
    
    data = await state.get_data()
    menu_mess = data.get('menu_mess')
    prev_mess = data.get('prev_mess')

    book_param = message.text
    
    if current_state == 'Name':       
        await state.update_data(book_name=book_param)
    elif current_state == 'Photo':
        await state.update_data(book_photo=book_param)
    elif current_state == 'Price':
        try:
            book_param = int(book_param)
        except ValueError:
            await message.answer('Введите цену числом!')
            return
        await state.update_data(book_price=book_param)

    await Edit_book.Choice.set()

    await menu_mess.edit_reply_markup(reply_markup=await menu_edit())
    await prev_mess.edit_reply_markup()
    await message.answer('✅')

# сохраняю изменения
@dp.callback_query_handler(text='save_changes', state=Edit_book.Choice)
async def save_changes(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    book_id = data.get('book_id')
    book_name = data.get('book_name')
    book_price = data.get('book_price')
    book_photo = data.get('book_photo')
    menu_mess = data.get('menu_mess')

    await db.change_book(book_id=book_id, inp_name=book_name,
                        inp_price=book_price, inp_photo=book_photo)

    await state.finish()

    await menu_mess.edit_reply_markup()
    await call.message.answer('Книга успешно измененна!')

# переход на предыдущее состояние
@dp.callback_query_handler(text='back', state=Edit_book.Name)
async def back_to_name(call: types.CallbackQuery, state: FSMContext):
    await Edit_book.Choice.set()

    data = await state.get_data()
    menu_mess = data.get('menu_mess')

    await menu_mess.edit_reply_markup(reply_markup=await menu_edit())
    await call.message.delete()
