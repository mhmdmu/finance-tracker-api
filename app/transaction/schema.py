from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class TransactionResponse(BaseModel):
    id: int
    account_id: int
    amount: Decimal
    type: str
    category_id: int
    transaction_date: date
    note: Optional[str]


class TransactionListResponse(BaseModel):
    items: list[TransactionResponse]
    total: int
    limit: int
    offset: int
    page: int


class TransactionCreate(BaseModel):
    type: str
    amount: Decimal = Field(gt=0)  # amount > 0
    category_id: Optional[int] = 1  # default is uncateogrized
    transaction_date: date
    note: Optional[str] = None


class TransactionFilters(BaseModel):
    category_id: Optional[int] = None
    type: Optional[str] = None
    date_to: Optional[date] = None
    date_from: Optional[date] = None
    # Pagination
    limit: int = Field(20, ge=1, le=100)
    offset: int = Field(0, ge=0)
