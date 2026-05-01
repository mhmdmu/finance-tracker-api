from asyncpg import Connection


async def get_all_accounts(user_id: int, conn: Connection):
    qurey = """
    SELECT *
    FROM accounts
    WHERE user_id = $1
    """

    return await conn.fetch(qurey, user_id)


async def get_account_by_id(id: int, user_id: int, conn: Connection):
    qurey = """
    SELECT *
    FROM accounts
    WHERE id = $1
    AND user_id = $2
    """

    return await conn.fetchrow(qurey, id, user_id)


async def create_account(user_id: int, type: str, name: str, conn: Connection):
    qurey = """
    INSERT INTO
    accounts(user_id, type, account_name)
    VALUES($1, $2, $3)
    RETURNING id, user_id, type, account_name
    """

    return await conn.fetchrow(qurey, user_id, type, name)


async def modify(id: int, type: str | None, name: str | None, conn):
    updated_fields = {
        "type": type,
        "account_name": name,
    }

    # keep only provided values
    updated_fields = {k: v for k, v in updated_fields.items() if v is not None}

    if not updated_fields:
        return None  # nothing to update

    set_clause = ", ".join(
        f"{key} = ${i + 2}" for i, key in enumerate(updated_fields.keys())
    )

    query = f"""
        UPDATE accounts
        SET {set_clause}
        WHERE id = $1
        RETURNING *
    """

    values = [id, *updated_fields.values()]

    return await conn.fetchrow(query, *values)


async def delete(id: int, conn: Connection):
    query = """
    DELETE from accounts
    WHERE id = $1
    """

    return await conn.fetchrow(query, id)
