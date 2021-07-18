
class Books:
    
    async def get_book(self, book_id):
        sql = 'SELECT * FROM Books WHERE id=$1'
        return await self.pool.fetchrow(sql, book_id)

    async def get_all_books(self):
        sql = 'SELECT * FROM Books ORDER BY id'
        return await self.pool.fetch(sql)
    
    async def add_book(self, name, price, photo):
        sql = 'INSERT INTO Books (name, price, photo) VALUES ($1, $2, $3)'
        await self.pool.execute(sql, name, price, photo)

    async def delete_book(self, book_id):
        sql = 'DELETE FROM Books WHERE id=$1'
        await self.pool.execute(sql, book_id)

    async def search_books(self, book_name):
        sql = "SELECT * FROM Books WHERE name ILIKE $1 ORDER BY name"
        return await self.pool.fetch(sql, book_name+'%')

    async def change_book(self, book_id, inp_name=None, inp_price=None, inp_photo=None):
        data = await self.get_book(book_id)
        book_name = data['name']
        book_price = data['price']
        book_photo = data['photo']

        if inp_name != None:
            book_name = inp_name
        if inp_price != None:
            book_price = inp_price
        if inp_photo != None:
            book_photo = inp_photo

        sql = 'UPDATE Books SET name=$1, price=$2, photo=$3 WHERE id=$4'

        await self.pool.execute(sql, book_name, book_price, book_photo, book_id)
