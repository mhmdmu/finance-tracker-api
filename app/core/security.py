from datetime import datetime, timedelta, timezone

import bcrypt
from jose import ExpiredSignatureError, JWTError, jwt

from app.core.config import settings


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.EXPIRE_MINUTES),
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_access_token(token: str) -> int:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
    except ExpiredSignatureError:
        raise ValueError("Token is expired")
    except JWTError:
        raise ValueError("Token is malformed")

    if user_id is None:
        raise ValueError("'sub' field is missing from the payload")

    return int(user_id)
