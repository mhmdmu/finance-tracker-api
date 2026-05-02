from asyncpg import Connection, InvalidTextRepresentationError

from app.account import repo
from app.core.exceptions import AccountNotFound, InvalidAccountType


async def get_all_accounts(user_id: int, conn: Connection):
    result = await repo.get_all_accounts(user_id, conn)

    return [dict(acc) for acc in result]


async def get_account(id: int, user_id: int, conn: Connection):
    account = await repo.get_account_by_id(id, user_id, conn)

    if account is None:
        raise AccountNotFound(id)

    return dict(account)


async def create_account(user_id: int, type: str, name: str, conn: Connection):
    try:
        account = await repo.create_account(user_id, type.lower(), name, conn)

        if account is None:
            raise AccountNotFound(id)

        return dict(account)
    except InvalidTextRepresentationError:
        raise InvalidAccountType()


async def modify_account(
    id: int,
    conn: Connection,
    type: str | None = None,
    name: str | None = None,
):
    account = await repo.modify(id, type, name, conn)

    if account is None:
        raise AccountNotFound(id)

    return dict(account)


async def delete_account(id: int, conn: Connection):
    deleted = await repo.delete(id, conn)

    if deleted is None:
        raise AccountNotFound(id)
