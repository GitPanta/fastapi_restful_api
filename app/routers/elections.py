from fastapi import APIRouter, Body, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from typing import Annotated

from app.core import schemas, dependencies, security
from app.db import crud, enums


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
) -> schemas.Election:
    return crud.create_election(db=db, election=election)


@router.post("/end/", response_model=schemas.ElectionResults)
def end_election_count(
    election_id: Annotated[int, Body()],
    db: Annotated[Session, Depends(dependencies.get_db)],
) -> list[schemas.ElectionResults]:
    return crud.end_election_count(db=db, election_id=election_id)


@router.put("/seats/", response_model=schemas.Election)
def set_election_seats(
    election: Annotated[schemas.ElectionUpdateSeats, Body()],
    db: Annotated[Session, Depends(dependencies.get_db)],
) -> schemas.Election:
    return crud.set_election_seats(db=db, election=election)