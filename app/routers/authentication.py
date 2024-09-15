from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated

from app.core import dependencies, schemas, security
from app.core.config import settings
from app.db import crud


router = APIRouter()


@router.post("/token/")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(dependencies.get_db),
) -> schemas.Token:
    user = crud.get_user_by_email(db, form_data.username)
    if user is None or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": form_data.username, "scopes": security.PERMISSIONS[user.role]},
        expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")