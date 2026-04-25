from asyncpg import create_pool
from core.config import settings

pool = None


async def connect() -> None:
    global pool
    pool = await create_pool(settings.DATABASE_URL, min_size=1, max_size=5)


async def disconnect() -> None:
    global pool
    if pool:
        await pool.close()


async def get_pool():
    return pool
