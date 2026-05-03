from asyncpg import Connection


async def get_all(user_id: int, conn: Connection):
    query = """
    SELECT * FROM categories
    WHERE user_id = $1
    OR user_id IS NULL
    """

    return await conn.fetch(query, user_id)


async def get_by_id(id: int, conn: Connection):
    query = """
    SELECT * FROM categories
    WHERE id = $1
    """

    return await conn.fetchrow(query, id)


async def create(user_id: int, name: str, conn: Connection):
    query = """
    INSERT INTO categories(user_id, name)
    VALUES ($1, $2)
    RETURNING *
    """

    return await conn.fetchrow(query, user_id, name)


async def update(id: int, new_name: str, conn: Connection):
    query = """
    UPDATE categories
    SET name = $1
    WHERE id = $2
    RETURNING *
    """

    return await conn.fetchrow(query, new_name, id)


async def delete(id: int, conn: Connection):
    query = """
    DELETE FROM categories
    WHERE id = $1
    RETURNING *
    """

    return await conn.fetchrow(query, id)
