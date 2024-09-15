from fastapi import APIRouter, Body, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from typing import Annotated

from app.core import schemas, dependencies, security
from app.db import crud, enums, models


router = APIRouter(
    prefix="/rosters",
    tags=["rosters"],
)


@router.get("/", response_model=list[schemas.Roster])
def get_rosters(db: Annotated[Session, Depends(dependencies.get_db)]) -> list[schemas.Roster]:
    rosters = crud.get_rosters(db)
    return rosters


@router.post("/", response_model=list[schemas.Roster])
def create_election_rosters(
    rosters: Annotated[list[schemas.RosterCreate], Body()],
    db: Annotated[Session, Depends(dependencies.get_db)],
    user: Annotated[
        models.User,
        Security(dependencies.get_current_user, scopes=security.PERMISSIONS[enums.UserRole.admin]),
    ],
) -> schemas.Roster:
    rosters = crud.create_rosters(db=db, rosters=rosters, user_id=user.id)
    return rosters