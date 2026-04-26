from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.core.security import verify_access_token

auth = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(auth)) -> int:
    try:
        return verify_access_token(token)
    except ValueError:
        raise HTTPException(401, detail="Authentication failed")
