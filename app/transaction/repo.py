from asyncpg import Connection

from app.transaction.schema import TransactionCreate, TransactionFilters


async def create_transaction(
    acc_id: int,
    transaction: TransactionCreate,
    conn: Connection,
):
    transaction_info = transaction.model_dump()

    columns = ", ".join(transaction_info.keys())

    # Total params = len(transaction_info) + 1; we have $1 (acc_id)
    placeholders = ", ".join(f"${i}" for i in range(2, len(transaction_info) + 2))

    query = f"""
    INSERT INTO transactions (account_id, {columns})
    VALUES ($1, {placeholders})
    RETURNING *
    """

    return await conn.fetchrow(query, acc_id, *transaction_info.values())


async def get_transaction_by_id(acc_id: int, trans_id: int, conn: Connection):
    query = """
    SELECT *
    FROM transactions
    WHERE account_id = $1
    AND id = $2
    """

    return await conn.fetchrow(query, acc_id, trans_id)


async def get_transactions_with_filters(
    acc_id: int, filters: TransactionFilters, conn: Connection
):
    conditions = ["account_id = $1"]
    values = [acc_id]
    counter = 2

    # skip pagination & sort fields
    filter_data = filters.model_dump(
        exclude_none=True, exclude={"limit", "offset", "sort"}
    )

    for key, value in filter_data.items():
        if key == "date_from":
            conditions.append(f"transaction_date >= ${counter}")
        elif key == "date_to":
            conditions.append(f"transaction_date <= ${counter}")
        else:
            conditions.append(f"{key} = ${counter}")

        values.append(value)
        counter += 1

    where_clause = " AND ".join(conditions)
    order_by = "DESC" if filters.sort == "desc" else "ASC"

    query = f"""
        SELECT *, count(*) OVER() as total_count
        FROM transactions
        WHERE {where_clause}
        ORDER BY transaction_date {order_by}
        LIMIT ${counter} OFFSET ${counter + 1}
    """

    values.extend([filters.limit, filters.offset])  # add pagination values

    return await conn.fetch(query, *values)


async def delete_transaction(acc_id: int, trans_id: int, conn: Connection):
    query = """
    DELETE FROM transactions
    WHERE id = $1
    AND account_id = $2
    RETURNING *
    """

    return await conn.fetchrow(query, trans_id, acc_id)
