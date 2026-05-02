from asyncpg import Connection
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.account.repo import check_account_exist_for_user
from app.core.database import get_conn
from app.core.exceptions import AccountNotFound
from app.core.security import verify_access_token

auth = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(auth)) -> int:
    try:
        return verify_access_token(token)
    except ValueError:
        raise HTTPException(401, detail="Authentication failed")


async def verify_account_ownership(
    acc_id: int,
    user_id: int = Depends(get_current_user),
    conn: Connection = Depends(get_conn),
):
    account = await check_account_exist_for_user(acc_id, user_id, conn)

    if account is None:
        raise AccountNotFound(acc_id)
