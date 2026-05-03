from asyncpg import Connection, ForeignKeyViolationError, InvalidTextRepresentationError

from app.category.repo import get_by_id
from app.core.exceptions import (
    AccountNotFound,
    CategoryNotFound,
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
    user_id: int,
    transaction: TransactionCreate,
    conn: Connection,
):
    category = await get_by_id(transaction.category_id or 1, conn)

    if category is None:
        raise CategoryNotFound(transaction.category_id)

    if category["user_id"] is not None and category["user_id"] != user_id:
        raise CategoryNotFound(transaction.category_id)

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

    if deleted is None:
        raise TransactionNotFound(trans_id)


async def calculate_cashflow_report(
    acc_id: int, month: int, year: int, conn: Connection
):
    rows = await repo.calculate_cashflow(acc_id, month, year, conn)
    result = {row["type"]: row["total"] for row in rows}
    income = result.get("income", 0)
    expense = result.get("expense", 0)

    # handle missing befor return
    return {
        "total_income": income,
        "total_expense": expense,
        "net_cashflow": income - expense,
        "month": month,
        "year": year,
    }


async def calculate_spending_report(
    acc_id: int, month: int, year: int, conn: Connection
):
    rows = await repo.calculate_spending_by_category(acc_id, month, year, conn)

    items = [
        {
            "category_name": row["name"],
            "total_expense": row["total"],
        }
        for row in rows
    ]

    return {"month": month, "year": year, "items": items}
