from app.database import pool


async def get_user_by_username(username: str):
    query = """
    SELECT *
    FROM users
    WHERE username = $1
    """

    async with pool.acquire() as conn:
        return await conn.fetchrow(query, username)


async def create_user(username: str, password: str):
    query = """
    INSERT INTO users(username, password)
    VALUES($1, $2)
    RETURNING id, username
    """

    async with pool.acquire() as conn:
        return await conn.fetchrow(query, username, password)
