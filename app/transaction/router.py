from typing import Annotated

from asyncpg import Connection
from fastapi import APIRouter, Depends, Query

from app.core.database import get_conn
from app.core.dependencies import get_current_user
from app.transaction import service
from app.transaction.schema import (
    TransactionCreate,
    TransactionFilters,
    TransactionListResponse,
    TransactionResponse,
)

transaction_router = APIRouter(prefix="/accounts", tags=["transactions"])


@transaction_router.get(
    "/{acc_id}/transactions", response_model=TransactionListResponse
)
async def read_all_transactions(
    acc_id: int,
    filters: Annotated[TransactionFilters, Query(), Depends()],
    conn: Connection = Depends(get_conn),
    _: int = Depends(get_current_user),  # protected
):
    return await service.get_transactions(acc_id, filters, conn)


@transaction_router.get(
    "/{acc_id}/transactions/{trans_id}", response_model=TransactionResponse
)
async def read_transaction(
    acc_id: int,
    trans_id: int,
    conn: Connection = Depends(get_conn),
    _: int = Depends(get_current_user),
):
    return await service.get_transaction(acc_id, trans_id, conn)


@transaction_router.post(
    "/{acc_id}/transactions",
    response_model=TransactionResponse,
    status_code=201,
)
async def create_transaction(
    acc_id: int,
    transaction: TransactionCreate,
    conn: Connection = Depends(get_conn),
    _: int = Depends(get_current_user),
):
    return await service.create_transaction(acc_id, transaction, conn)


@transaction_router.delete("/{acc_id}/transactions/{trans_id}", status_code=204)
async def delete(
    acc_id: int,
    trans_id: int,
    conn: Connection = Depends(get_conn),
    _: int = Depends(get_current_user),
):
    await service.delete_transaction(acc_id, trans_id, conn)
