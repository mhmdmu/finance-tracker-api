from decimal import Decimal

from pydantic import BaseModel


class AccountResponse(BaseModel):
    id: int
    user_id: int
    type: str
    account_name: str
    balance: Decimal = Decimal(0)


class AccountCreate(BaseModel):
    type: str
    account_name: str


class AccountModify(BaseModel):
    type: str | None = None
    account_name: str | None = None
