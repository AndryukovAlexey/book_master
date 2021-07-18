from aiogram import types
from aiogram.utils.deep_linking import get_start_link

from loader import dp, db
from filters import AvailabilityCall
from keyboards.inline import inline_show_book


@dp.inline_handler(AvailabilityCall())
async def book_query(query: types.InlineQuery):
    books = await db.search_books(str(query.query))
    results = []
    
    for book in books:
        results.append(types.InlineQueryResultArticle(
                        id=book['id'],
                        title=book['name'],
                        description=f"цена: {book['price']}",
                        reply_markup = await inline_show_book(book['id']),
                        input_message_content=types.InputTextMessageContent(
                                message_text=f"книга: {book['name']} \nцена: {book['price']}"),                      
                        thumb_url=book['photo']
                    ))               
    
    await query.answer(results)
