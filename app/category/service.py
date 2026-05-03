from asyncpg import Connection

from app.category import repo
from app.core.exceptions import CategoryNotFound


async def get_categories(user_id: int, conn: Connection):
    categories = await repo.get_all(user_id, conn)

    return [dict(cat) for cat in categories]


async def create_category(user_id: int, name: str, conn: Connection):
    category = await repo.create(user_id, name, conn)

    if category is not None:
        return dict(category)


async def update_category(id: int, name: str, conn: Connection):
    updated = await repo.update(id, name, conn)

    if updated is None:
        raise CategoryNotFound(id)

    return dict(updated)


async def delete_category(id: int, conn: Connection):
    deleted = await repo.delete(id, conn)

    if deleted is None:
        raise CategoryNotFound(id)
