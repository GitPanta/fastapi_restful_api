import jwt
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from pydantic import ValidationError
from sqlalchemy.orm import Session

from . import schemas
from .config import settings
from app.db import crud, enums
from app.db.database import SessionLocal, engine


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login",
    scopes={
        enums.UserRole.user: "Can view election results",
        enums.UserRole.admin: "User permissiones and can set election results",
        enums.UserRole.super_admin: "Admin permissions and can add users",
    }
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> schemas.User:
    username = verify_permissions(security_scopes=security_scopes, token=token)
    user = crud.get_user_by_email(db=db, email=username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found"
        )
    return user


def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")



def verify_permissions(security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value}
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload['sub']
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = schemas.TokenData(scopes=token_scopes, username=username)
    except (InvalidTokenError, ValidationError):
        raise credentials_exception
    
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return username