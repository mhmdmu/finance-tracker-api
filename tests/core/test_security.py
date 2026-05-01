from datetime import datetime, timedelta, timezone

import pytest
from jose import jwt

import app.core.security as security
from app.core.config import settings


@pytest.fixture
def password():
    plain = "password"
    return plain, security.hash_password(plain)


#
# Helper to generate JWTs for testing edge cases (expired, missing sub, etc.)
#
def make_token(sub=None, expired=False):
    curr_time = datetime.now(timezone.utc)
    time_delta = timedelta(minutes=settings.EXPIRE_MINUTES)

    if expired:
        time_delta = -time_delta

    payload = {
        "exp": curr_time + time_delta,
    }

    if sub is not None:
        payload["sub"] = sub

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


#
# password hashing
#
def test_hash_password(password):
    plain, hashed = password

    assert plain != hashed, "hash_password returned the plain text unchanged"
    assert hashed.startswith("$2b$"), "hash_password did not return a bcrypt hash"


def test_verify_password_correct(password):
    plain, hashed = password

    assert security.verify_password(plain, hashed), (
        "verify_password did not return True on matched passwords"
    )


def test_verify_password_wrong(password):
    _, hashed = password
    wrong = "passw0rd"

    assert not security.verify_password(wrong, hashed), (
        "verify_password did not return False on different passwords"
    )


#
# token creation
#
def test_create_access_token():
    token = security.create_access_token(100)
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert "sub" in payload, "'sub' claim is missing from the payload"
    assert "exp" in payload, "'exp' claim is missing from the payload"


#
# token validation
#
def test_verify_access_token_returns_correct_user_id():
    token = security.create_access_token(100)
    user_id = security.verify_access_token(token)

    assert isinstance(user_id, int), "verify_access_token didn't return int"
    assert user_id == 100, "verify_access_token returned a wrong user_id"


def test_verify_access_token_raises_on_malformed_token():
    token = security.create_access_token(100)

    with pytest.raises(ValueError, match="malformed"):
        malformed = token + "noise"
        security.verify_access_token(malformed)


def test_verify_access_token_raises_on_expired_token():
    with pytest.raises(ValueError, match="expired"):
        expired = make_token(expired=True, sub="100")
        security.verify_access_token(expired)


def test_verify_access_token_raises_on_missing_sub():
    with pytest.raises(ValueError, match="missing"):
        token = make_token()
        security.verify_access_token(token)
