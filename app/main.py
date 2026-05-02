from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import app.core.database as db
from app.account.router import acc_router
from app.auth.router import auth_router
from app.core.exceptions import (
    AccountNotFound,
    AuthenticationFailed,
    DuplicateUsername,
    InvalidAccountType,
    InvalidTransactionType,
    TransactionNotFound,
)
from app.transaction.router import transaction_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    app.state.pool = await db.connect()
    yield
    # On shutdown
    await db.disconnect(app.state.pool)


app = FastAPI(lifespan=lifespan)

# Routers
routers_prefix = "/api/v1"
app.include_router(auth_router, prefix=routers_prefix)
app.include_router(acc_router, prefix=routers_prefix)
app.include_router(transaction_router, prefix=routers_prefix)


# Exception handling
@app.exception_handler(AuthenticationFailed)
async def auth_failed_handler(_: Request, e: AuthenticationFailed):
    return JSONResponse(status_code=401, content={"detail": str(e)})


@app.exception_handler(DuplicateUsername)
async def duplicate_username_handler(_: Request, e: DuplicateUsername):
    return JSONResponse(status_code=409, content={"detail": str(e)})


@app.exception_handler(InvalidAccountType)
async def invalid_account_type_handler(_: Request, e: InvalidAccountType):
    return JSONResponse(status_code=422, content={"detail": str(e)})


@app.exception_handler(AccountNotFound)
async def delete_not_existing_account_handler(_: Request, e: AccountNotFound):
    return JSONResponse(status_code=404, content={"detail": str(e)})


@app.exception_handler(TransactionNotFound)
async def delete_not_existing_transaction_handler(_: Request, e: TransactionNotFound):
    return JSONResponse(status_code=404, content={"detail": str(e)})


@app.exception_handler(InvalidTransactionType)
async def invalid_transaction_type_handler(_: Request, e: InvalidTransactionType):
    return JSONResponse(status_code=422, content={"detail": str(e)})
