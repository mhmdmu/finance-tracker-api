from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_conn
from app.schemas.user import UserRegister, UserResponse
from app.services import auth

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(
    request: Annotated[OAuth2PasswordRequestForm, Depends()], conn=Depends(get_conn)
):
    token = await auth.login(request.username, request.password, conn)

    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", response_model=UserResponse)
async def register(request: UserRegister, conn=Depends(get_conn)):
    return await auth.register(request.username, request.password, conn)
