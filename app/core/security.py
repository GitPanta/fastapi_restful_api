import jwt
from enum import Enum
from typing import Annotated
from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core import dependencies, schemas
from app.core.config import settings
from app.db import crud, enums


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta
    to_encode.update({"exp": expire})
    print("TO ENCODE", to_encode)
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


class Scopes(Enum):
    user = "user"
    admin = "admin"
    super_admin = "super"


PERMISSIONS = {
    enums.UserRole.user: [Scopes.user.value],
    enums.UserRole.admin: [Scopes.user.value, Scopes.admin.value],
    enums.UserRole.super_admin: [Scopes.user.value, Scopes.admin.value, Scopes.super_admin.value],
}