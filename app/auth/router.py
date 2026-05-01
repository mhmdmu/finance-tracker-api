from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import service
from app.auth.user_schema import UserRegister, UserResponse
from app.core.database import get_conn

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(
    request: Annotated[OAuth2PasswordRequestForm, Depends()], conn=Depends(get_conn)
):
    token = await service.login(request.username, request.password, conn)

    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", response_model=UserResponse)
async def register(request: UserRegister, conn=Depends(get_conn)):
    return await service.register(request.username, request.password, conn)
