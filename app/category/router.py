from asyncpg import Connection
from fastapi import APIRouter, Body, Depends

from app.category import service
from app.category.schema import CategoryResponse
from app.core.database import get_conn
from app.core.dependencies import get_current_user, verify_category_ownership

category_router = APIRouter(prefix="/categories", tags=["categories"])


@category_router.get("", response_model=list[CategoryResponse])
async def read_categories(
    conn: Connection = Depends(get_conn),
    user_id: int = Depends(get_current_user),
):
    return await service.get_categories(user_id, conn)


@category_router.post("", status_code=201, response_model=CategoryResponse)
async def create_custom_category(
    name: str = Body(embed=True),
    conn: Connection = Depends(get_conn),
    user_id: int = Depends(get_current_user),
):
    return await service.create_category(user_id, name, conn)


@category_router.patch("/{cat_id}")
async def update_category_name(
    cat_id: int,
    name: str = Body(embed=True),
    conn: Connection = Depends(get_conn),
    _=Depends(verify_category_ownership),
):
    return await service.update_category(cat_id, name, conn)


@category_router.delete("/{cat_id}", status_code=204)
async def delete_category(
    cat_id: int,
    conn: Connection = Depends(get_conn),
    _=Depends(verify_category_ownership),
):
    await service.delete_category(cat_id, conn)
