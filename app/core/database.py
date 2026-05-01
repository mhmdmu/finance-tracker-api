from asyncpg import Pool, create_pool
from fastapi import Request

from app.core.config import settings


async def connect() -> Pool:
    return await create_pool(settings.DATABASE_URL, min_size=1, max_size=5)


async def disconnect(pool: Pool) -> None:
    await pool.close()


async def get_conn(request: Request):
    pool = request.app.state.pool

    if pool is None:
        raise RuntimeError("Database pool is not initialized")

    async with pool.acquire() as conn:
        async with conn.transaction():
            yield conn
