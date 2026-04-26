import pytest
from pydantic import ValidationError

from app.schemas.user import UserRegister


#
# Helper function to create user model, defaults to a valid user
#
def create_user(username="USER", password="P@$$w0rd"):
    return UserRegister(username=username, password=password)


def test_user_creation_on_success():
    assert create_user().username.islower(), (
        "Username wasn't normalized to be lowercase"
    )


#
# Username validation
#
def test_username_not_start_with_letters():
    invalid_usernames = ["0aaaaaa", "_aaaaaaa"]

    for username in invalid_usernames:
        with pytest.raises(ValidationError, match="pattern_mismatch"):
            create_user(username=username)


def test_username_too_short():
    with pytest.raises(ValidationError, match="too_short"):
        create_user(username="a")


def test_username_too_long():
    with pytest.raises(ValidationError, match="too_long"):
        create_user(username="a" * 100)


def test_username_consecutive_underscores():
    with pytest.raises(ValidationError, match="consecutive underscores"):
        create_user(username="user__")


#
# Password validation
#
def test_password_too_short():
    with pytest.raises(ValidationError, match="too_short"):
        create_user(password="123")


def test_password_too_long():
    with pytest.raises(ValidationError, match="too_long"):
        create_user(password="p" * 100)


def test_password_no_uppercase():
    with pytest.raises(ValidationError, match="uppercase"):
        create_user(password="abcdefjhi12")


def test_password_no_lowercase():
    with pytest.raises(ValidationError, match="lowercase"):
        create_user(password="ABCDEFJHI12")


def test_password_no_digit():
    with pytest.raises(ValidationError, match="digit"):
        create_user(password="ABCDEFJHijk")
