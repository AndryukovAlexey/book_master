import asyncpg

import random
import string


class Users:

    @staticmethod
    async def create_ref_link(length=10):
        symbols = string.ascii_letters + string.digits
        link = ''.join(random.sample(symbols, length))
        return link

    async def add_user(self, user_id):
        sql = 'INSERT INTO Users (id, balance, ref_link) VALUES ($1, $2, $3)'
        balance = 0
        ref_link = await self.create_ref_link()
        try:
            await self.pool.execute(sql, user_id, balance, ref_link)
        except asyncpg.exceptions.UniqueViolationError as err:
            pass
            
    async def get_user(self, user_id):
        sql = 'SELECT * FROM Users WHERE id=$1'
        return await self.pool.fetchrow(sql, user_id)

    async def check_ref_link(self, link):
        sql = 'SELECT id, balance FROM Users WHERE ref_link=$1'
        return await self.pool.fetchrow(sql, link)
    
    async def get_balance(self, user_id):
        sql = 'SELECT balance FROM Users WHERE id=$1'
        return await self.pool.fetchrow(sql, user_id)
    
    async def ref_point(self, user_id, balance):
        balance += 100
        sql = 'UPDATE Users SET balance=$1 WHERE id=$2'
        await self.pool.execute(sql, balance, user_id)

