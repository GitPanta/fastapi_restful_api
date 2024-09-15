from fastapi import APIRouter, Body, Depends, HTTPException, Security, status
from sqlalchemy.orm import Session
from typing import Annotated

from app.core import schemas, dependencies, security
from app.db import crud, enums, models


router = APIRouter(
    prefix="/elections",
    tags=["elections"],
)


@router.get("/", response_model=list[schemas.Election])
def get_elections(db: Annotated[Session, Depends(dependencies.get_db)]) -> list[schemas.Election]:
    elections = crud.get_elections(db)
    return elections


@router.post("/", response_model=schemas.Election)
def create_election(
    election: Annotated[schemas.ElectionCreate, Body()],
    db: Annotated[Session, Depends(dependencies.get_db)],
    user: Annotated[
        models.User,
        Security(dependencies.get_current_user, scopes=security.PERMISSIONS[enums.UserRole.admin]),
    ]
) -> schemas.Election:
    return crud.create_election(db=db, election=election, user_id=user.id)


@router.post("/end/", response_model=schemas.ElectionResults)
def end_election_count(
    election_id: Annotated[int, Body()],
    db: Annotated[Session, Depends(dependencies.get_db)],
    user: Annotated[models.User, Security(dependencies.get_current_user, scopes=security.PERMISSIONS[enums.UserRole.admin])],
) -> list[schemas.ElectionResults]:
    election_results = crud.end_election_count(db=db, election_id=election_id, user_id=user.id)
    if election_results is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID"
        )
    return election_results


@router.put("/seats/", response_model=schemas.Election)
def set_election_seats(
    election: Annotated[schemas.ElectionUpdateSeats, Body()],
    db: Annotated[Session, Depends(dependencies.get_db)],
    user: Annotated[models.User, Security(dependencies.get_current_user, scopes=security.PERMISSIONS[enums.UserRole.admin])],
) -> schemas.Election:
    db_election = crud.set_election_seats(db=db, election=election)
    if db_election is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID"
        )
    return db_election