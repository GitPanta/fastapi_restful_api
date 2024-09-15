from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from typing import Annotated

from app.core import schemas, dependencies, security
from app.db import crud, enums

# router = APIRouter()

router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)


@router.get("/")
def read_users(
    token: Annotated[str, Security(dependencies.oauth2_scheme, scopes=[enums.UserRole.super_admin])]
):
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/me/", response_model=schemas.User)
def get_current_user(
    current_user: Annotated[
        schemas.User,
        Security(dependencies.get_current_user, scopes=security.PERMISSIONS[enums.UserRole.user])],
) -> schemas.User:
    return current_user


@router.get("/{username}")
def read_user(username: str):
    return {"username": username}


@router.post("/", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate,
    db: Annotated[Session, Depends(dependencies.get_db)],
) -> schemas.User:
    db_user = crud.get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)