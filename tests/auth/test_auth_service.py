from unittest.mock import AsyncMock, patch

import pytest
from asyncpg.exceptions import UniqueViolationError

from app.auth import auth_service
from app.core.exceptions import AuthenticationFailed, DuplicateUsername
from app.core.security import hash_password


@pytest.fixture
def mock_get_user():
    patched_func = "app.auth.auth_service.user_repo.get_user_by_username"

    with patch(patched_func, new_callable=AsyncMock) as mock:
        yield mock


@pytest.fixture
def mock_create_user():
    patched_func = "app.auth.auth_service.user_repo.create_user"

    with patch(patched_func, new_callable=AsyncMock) as mock:
        yield mock


@pytest.mark.asyncio
async def test_login_success(mock_get_user):
    mock_get_user.return_value = {
        "id": 1,
        "username": "user1",
        "password": hash_password("pass1"),
    }

    token = await auth_service.login("user1", "pass1", None)

    assert token is not None, "login did not return a token"


@pytest.mark.asyncio
async def test_login_on_user_not_found(mock_get_user):
    mock_get_user.return_value = None

    with pytest.raises(AuthenticationFailed, match="Invalid credentials"):
        await auth_service.login("abc", "abc", None)


@pytest.mark.asyncio
async def test_login_on_wrong_password(mock_get_user):
    mock_get_user.return_value = {
        "id": 1,
        "username": "user1",
        "password": hash_password("pass1"),
    }

    with pytest.raises(AuthenticationFailed, match="Invalid credentials"):
        await auth_service.login("user1", "abc", None)


@pytest.mark.asyncio
async def test_register_on_success(mock_create_user):
    mock_create_user.return_value = {
        "id": 1,
        "username": "new",
    }

    result = await auth_service.register("new", "pass", None)

    assert result["username"] == "new", "user created with different username"
    mock_create_user.assert_called_once()


@pytest.mark.asyncio
async def test_register_duplicate_username(mock_create_user):

    mock_create_user.side_effect = UniqueViolationError()

    with pytest.raises(DuplicateUsername, match="Registeration failed"):
        await auth_service.register("user1", "pass1", None)
