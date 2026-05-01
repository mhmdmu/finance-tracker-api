from asyncpg import Connection
from fastapi import APIRouter, Depends

from app.account import service
from app.account.schema import AccountCreate, AccountModify, AccountResponse
from app.core.database import get_conn
from app.core.dependencies import get_current_user

acc_router = APIRouter(prefix="/accounts", tags=["account"])


@acc_router.get("/{acc_id}", response_model=AccountResponse)
async def read_account_for_current_user(
    acc_id: int,
    curr_user_id: int = Depends(get_current_user),
    conn: Connection = Depends(get_conn),
):
    return await service.get_account(acc_id, curr_user_id, conn)


@acc_router.get("", response_model=list[AccountResponse])
async def read_all_accounts_current_user(
    user_id: int = Depends(get_current_user), conn: Connection = Depends(get_conn)
):
    return await service.get_all_accounts(user_id, conn)


@acc_router.post("", response_model=AccountResponse, status_code=201)
async def create_account(
    account_info: AccountCreate,
    conn: Connection = Depends(get_conn),
    user_id: int = Depends(get_current_user),  # protected
):
    return await service.create_account(
        user_id,
        account_info.type,
        account_info.account_name,
        conn,
    )


@acc_router.patch("/{id}", response_model=AccountResponse)
async def modify_account_info(
    id: int,
    account_info: AccountModify,
    conn: Connection = Depends(get_conn),
    _: int = Depends(get_current_user),  # protected
):
    return await service.modify_account(
        id,
        conn,
        type=account_info.type,
        name=account_info.account_name,
    )


@acc_router.delete("/{id}", status_code=204)
async def delete_account(
    id: int,
    conn: Connection = Depends(get_conn),
    _: int = Depends(get_current_user),  # protected
):
    await service.delete_account(id, conn)
