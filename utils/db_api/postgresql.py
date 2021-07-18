import asyncio
import asyncpg

from data import config
from .users import Users
from .books import Books


class Database(Users, Books):
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.pool: asyncio.pool.Pool = loop.run_until_complete(           
            asyncpg.create_pool(
                database = config.DATABASE_NAME,
                user = config.PGUSER,
                password = config.PGPASSWORD,
                host = config.DBHOST         
            )
        )
          
    async def create_tables(self):
        await self.create_table_users()
        await self.create_table_books()

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id INT NOT NULL UNIQUE,
            balance INT,
            ref_link VARCHAR(255) NOT NULL,
            PRIMARY KEY (id)
        )
        
        """
        await self.pool.execute(sql)

    async def create_table_books(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Books (
            id SERIAL NOT NULL,
            name VARCHAR(255) NOT NULL,
            price INT NOT NULL,
            photo VARCHAR(255) NOT NULL,
            PRIMARY KEY (id)
        )
        
        """
        await self.pool.execute(sql)

