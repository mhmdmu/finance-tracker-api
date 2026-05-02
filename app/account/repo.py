from asyncpg import Connection


async def get_all_accounts(user_id: int, conn: Connection):
    query = """
    SELECT
        a.*,
        COALESCE(
            SUM(
                CASE
                    WHEN t.type = 'income' THEN t.amount
                    WHEN t.type = 'expense' THEN -t.amount
                    ELSE 0
                END
            ),
            0
        ) AS balance
    FROM accounts a
    LEFT JOIN transactions t ON t.account_id = a.id
    WHERE a.user_id = $1
    GROUP BY a.id
    """

    return await conn.fetch(query, user_id)


async def get_account_by_id(id: int, conn: Connection):
    query = """
    SELECT
        a.*,
        COALESCE(
            SUM(
                CASE
                    WHEN t.type = 'income' THEN t.amount
                    WHEN t.type = 'expense' THEN -t.amount
                    ELSE 0
                END
            ),
            0
        ) AS balance
    FROM accounts a
    LEFT JOIN transactions t ON t.account_id = a.id
    WHERE a.id = $1
    GROUP BY a.id
    """

    return await conn.fetchrow(query, id)


async def create_account(user_id: int, type: str, name: str, conn: Connection):
    query = """
    INSERT INTO
    accounts(user_id, type, account_name)
    VALUES($1, $2, $3)
    RETURNING id, user_id, type, account_name
    """

    return await conn.fetchrow(query, user_id, type, name)


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
    RETURNING *
    """

    return await conn.fetchrow(query, id)


async def check_account_exist_for_user(id: int, user_id: int, conn: Connection):
    query = "SELECT 1 FROM accounts WHERE id = $1 AND user_id = $2"

    return await conn.fetchrow(query, id, user_id)
