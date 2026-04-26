from asyncpg.exceptions import UniqueViolationError

from app.core import security
from app.repositories import user as user_repo


async def login(username: str, password: str):
    user = await user_repo.get_user_by_username(username)
    auth_failed_exception = ValueError("Authentication failed")

    if user is None:
        raise auth_failed_exception

    if not security.verify_password(password, user["password"]):
        raise auth_failed_exception

    return security.create_access_token(user["id"])


async def register(username: str, password: str):
    try:
        return await user_repo.create_user(username, security.hash_password(password))
    except UniqueViolationError:
        raise ValueError("Username already exists")
