from os import getenv

from asyncpg import create_pool
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = getenv("DATABASE_URL")

pool = None


async def connect() -> None:
    global pool
    pool = await create_pool(DATABASE_URL, min_size=1, max_size=5)


async def disconnect() -> None:
    global pool
    if pool:
        await pool.close()


async def get_pool():
    return pool
