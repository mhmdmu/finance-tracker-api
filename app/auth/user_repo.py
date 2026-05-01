async def get_user_by_username(username: str, conn):
    query = """
    SELECT *
    FROM users
    WHERE username = $1
    """

    return await conn.fetchrow(query, username)


async def create_user(username: str, password: str, conn):
    query = """
    INSERT INTO users(username, password)
    VALUES($1, $2)
    RETURNING id, username
    """

    return await conn.fetchrow(query, username, password)
