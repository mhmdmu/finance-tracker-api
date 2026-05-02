from asyncpg import Connection, ForeignKeyViolationError, InvalidTextRepresentationError

from app.core.exceptions import (
    AccountNotFound,
    InvalidTransactionType,
    TransactionNotFound,
)
from app.transaction import repo
from app.transaction.schema import TransactionCreate, TransactionFilters


async def get_transactions(acc_id: int, filters: TransactionFilters, conn: Connection):
    rows = await repo.get_transactions_with_filters(acc_id, filters, conn)

    # first row (window function)
    total_records = rows[0]["total_count"] if rows else 0

    current_page = (filters.offset // filters.limit) + 1

    return {
        "items": [dict(r) for r in rows],
        "total": total_records,
        "limit": filters.limit,
        "offset": filters.offset,
        "page": current_page,
    }


async def get_transaction(acc_id: int, trans_id: int, conn: Connection):
    transaction = await repo.get_transaction_by_id(acc_id, trans_id, conn)

    if transaction is None:
        raise TransactionNotFound(trans_id)

    return dict(transaction)


async def create_transaction(
    acc_id: int,
    transaction: TransactionCreate,
    conn: Connection,
):
    try:
        created = await repo.create_transaction(acc_id, transaction, conn)

        if created is None:
            raise AccountNotFound(acc_id)
    except InvalidTextRepresentationError:
        raise InvalidTransactionType()
    except ForeignKeyViolationError:  # account_id doesn't exist
        raise AccountNotFound(acc_id)

    return dict(created)


async def delete_transaction(acc_id: int, trans_id: int, conn: Connection):
    deleted = await repo.delete_transaction(acc_id, trans_id, conn)
    print(f"{deleted=}")

    if deleted is None:
        raise TransactionNotFound(trans_id)
