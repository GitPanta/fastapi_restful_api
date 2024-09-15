from fastapi import APIRouter, Body, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from typing import Annotated

from app.core import schemas, dependencies, security
from app.db import crud, enums


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
) -> schemas.Roster:
    rosters = crud.create_rosters(db=db, rosters=rosters)
    return rosters