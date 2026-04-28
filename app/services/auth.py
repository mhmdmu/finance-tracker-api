from asyncpg.exceptions import UniqueViolationError

from app.core import security
from app.exceptions import AuthenticationFailed, DuplicateUsername
from app.repositories import user as user_repo


async def login(username: str, password: str, conn):
    user = await user_repo.get_user_by_username(username, conn)

    if user is None or not security.verify_password(password, user["password"]):
        raise AuthenticationFailed()

    return security.create_access_token(user["id"])


async def register(username: str, password: str, conn):
    try:
        return dict(
            await user_repo.create_user(
                username,
                security.hash_password(password),
                conn,
            )
        )
    except UniqueViolationError:
        raise DuplicateUsername(username)
