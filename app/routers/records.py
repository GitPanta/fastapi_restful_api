from fastapi import APIRouter, Body, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from typing import Annotated

from app.core import schemas, dependencies, security
from app.db import crud, enums

router = APIRouter(
    prefix="/records",
    tags=["records"],
)


@router.get("/", response_model=list[schemas.Record])
def get_records(
    db: Annotated[Session, Depends(dependencies.get_db)]
) -> list[schemas.Record]:
    records = crud.get_records(db)
    return records


@router.get("/{election_id}", response_model=list[schemas.Record])
def get_records_by_election(
    election_id: int,
    db: Annotated[Session, Depends(dependencies.get_db)],
) -> list[schemas.Record]:
    records = crud.get_records_by_election(db=db, election_id=election_id)
    return records


@router.post("/", response_model=list[schemas.Record])
def create_records(
    records: Annotated[list[schemas.RecordCreate], Body()],
    db: Annotated[Session, Depends(dependencies.get_db)],
    current_user: Annotated[
        str,
        Security(dependencies.verify_permissions, scopes=security.PERMISSIONS[enums.UserRole.admin]),
    ],
) -> list[schemas.Record]:
    records = crud.create_records(db=db, records=records)
    return records


@router.put("/")
def set_roster_votes_count(
    record: Annotated[schemas.RecordBase, Body()],
    db: Annotated[Session, Depends(dependencies.get_db)],
    current_user: Annotated[
        str,
        Security(dependencies.verify_permissions, scopes=security.PERMISSIONS[enums.UserRole.admin]),
    ],
) -> None:
    crud.set_record_votes_count(db=db, record=record)