import re

from pydantic import BaseModel, Field, field_validator


class UserRegister(BaseModel):
    username: str = Field(
        min_length=4,
        max_length=20,
        pattern=r"^[a-zA-Z][a-zA-Z0-9_]*$",
    )
    password: str = Field(min_length=8, max_length=64)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str):
        if "__" in v:
            raise ValueError("No consecutive underscores allowed")

        return v.lower()  # normalize

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str):
        if not re.search(r"[a-z]", v):
            raise ValueError("Must contain lowercase letter")

        if not re.search(r"[A-Z]", v):
            raise ValueError("Must contain uppercase letter")

        if not re.search(r"\d", v):
            raise ValueError("Must contain a digit")

        return v


class UserResponse(BaseModel):
    id: int
    username: str
