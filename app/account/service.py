from asyncpg import Connection, InvalidTextRepresentationError

from app.account import repo
from app.core.exceptions import AccountNotFound, InvalidAccountType


async def get_all_accounts(user_id: int, conn: Connection):
    result = await repo.get_all_accounts(user_id, conn)

    return [dict(acc) for acc in result]


async def get_account(id: int, user_id: int, conn: Connection):
    return dict(await repo.get_account_by_id(id, user_id, conn))


async def create_account(user_id: int, type: str, name: str, conn: Connection):
    try:
        return dict(await repo.create_account(user_id, type.lower(), name, conn))
    except InvalidTextRepresentationError:
        raise InvalidAccountType()


async def modify_account(
    id: int,
    conn: Connection,
    type: str | None = None,
    name: str | None = None,
):
    return dict(await repo.modify(id, type, name, conn))


async def delete_account(id: int, conn: Connection):
    deleted = await repo.delete(id, conn)

    if deleted is None:
        raise AccountNotFound(id)
