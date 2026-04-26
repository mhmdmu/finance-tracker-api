from unittest.mock import AsyncMock, patch

import pytest
from _pytest.monkeypatch import V
from asyncpg.exceptions import UniqueViolationError

from app.core.security import hash_password
from app.services import auth


@pytest.fixture
def mock_get_user():
    patched_func = "app.services.auth.user_repo.get_user_by_username"

    with patch(patched_func, new_callable=AsyncMock) as mock:
        yield mock


@pytest.fixture
def mock_create_user():
    patched_func = "app.services.auth.user_repo.create_user"

    with patch(patched_func, new_callable=AsyncMock) as mock:
        yield mock


@pytest.mark.asyncio
async def test_login_success(mock_get_user):
    mock_get_user.return_value = {
        "id": 1,
        "username": "user1",
        "password": hash_password("pass1"),
    }

    token = await auth.login("user1", "pass1")

    assert token is not None, "login did not return a token"


@pytest.mark.asyncio
async def test_login_on_user_not_found(mock_get_user):
    mock_get_user.return_value = None

    with pytest.raises(ValueError, match="not found"):
        await auth.login("abc", "abc")


@pytest.mark.asyncio
async def test_login_on_wrong_password(mock_get_user):
    mock_get_user.return_value = {
        "id": 1,
        "username": "user1",
        "password": hash_password("pass1"),
    }

    with pytest.raises(ValueError, match="Invalid password"):
        await auth.login("user1", "abc")


@pytest.mark.asyncio
async def test_register_on_success(mock_create_user):
    mock_create_user.return_value = {
        "id": 1,
        "username": "new",
    }

    result = await auth.register("new", "pass")

    assert result["username"] == "new", "user created with different username"
    mock_create_user.assert_called_once()


@pytest.mark.asyncio
async def test_register_duplicate_username(mock_create_user):

    mock_create_user.side_effect = UniqueViolationError()

    with pytest.raises(ValueError, match="already exists"):
        await auth.register("user1", "pass1")
