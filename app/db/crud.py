from sqlalchemy import insert
from sqlalchemy.orm import Session

from . import models
from app.core import schemas, security


def create_election(db: Session, election: schemas.ElectionCreate, user_id: int) -> models.Election:
    db_election = models.Election(
        description=election.description,
        seats_amount=election.seats_amount,
        is_active=election.is_active,
        created_by=user_id,
        modified_by=user_id,
    )
    db.add(db_election)
    db.commit()
    db.refresh(db_election)
    return db_election


def get_elections(db: Session) -> list[models.Election]:
    return db.query(models.Election).all()


def end_election_count(db: Session, election_id: int, user_id: int) -> schemas.ElectionResults:
    db_election = db.query(models.Election).filter(models.Election.id == election_id).first()
    
    if db_election is None:
        return None
    
    db_records = db.query(models.Record).filter(models.Record.election_id == election_id).all()
    
    seats_count = db_election.seats_amount
    
    election_records = []
    roster_seats = {}
    roster_temp_cacl = {}
    
    while seats_count > 0:
        max_votes = 0
        seats_count -= 1
        next_seat = 0
        for record in db_records:
            roster_id = record.roster_id
            if roster_id not in roster_seats:
                roster_seats[roster_id] = 0
                roster_temp_cacl[roster_id] = record.votes_amount
            x = record.votes_amount // (roster_seats[roster_id] + 1)
            roster_temp_cacl[roster_id] = x
            if x > max_votes:
                max_votes = x
                next_seat = roster_id
        roster_seats[next_seat] += 1
        max_votes = 0
    for record in db_records:
        record.roster_seats_amount = roster_seats[record.roster_id]
        
        roster = db.query(models.Roster).filter(models.Roster.id == record.roster_id).first()

        result = schemas.ElectionRecord(
            roster_id = roster.id,
            roster_name = roster.name,
            roster_seats_amount = record.roster_seats_amount,
            roster_votes_amount = record.votes_amount,
        )
        election_records.append(result)
    
    db_election.is_active = False
    db_election.modified_by = user_id
    db.commit()
    election_results = schemas.ElectionResults(
        election_id = election_id,
        election_seats_amount = db_election.seats_amount,
        results = election_records,
    )
    return election_results


def set_election_seats(db: Session, election: schemas.ElectionUpdateSeats, user_id: int) -> models.Election:
    db_election = db.query(models.Election).filter(models.Election.id == election.id).first()
    if db_election is None:
        return None
    db_election.seats_amount = election.seats_amount
    db_election.modified_by = user_id
    db.commit()
    return db_election


def create_records(db: Session, records: list[schemas.RecordCreate]) -> list[models.Record]:
    db_records = []
    for record in records:
        db_record = models.Record(
            election_id=record.election_id,
            roster_id=record.roster_id,
            votes_amount=record.votes_amount,
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        db_records.append(db_record)
    return db_records


def get_records(db: Session):
    return db.query(models.Record).all()


def get_records_by_election(db: Session, election_id: int) -> list[models.Record]:
    return db.query(models.Record).filter(models.Record.election_id == election_id).all()


def set_record_votes_count(db: Session, record: schemas.RecordBase) -> None:
    db_record = db.query(models.Record).filter(
        models.Record.election_id == record.election_id,
        models.Record.roster_id == record.roster_id,
    ).first()
    db_record.votes_amount = record.votes_amount
    db.commit()


def create_roster(db: Session, roster: schemas.RosterCreate, user_id: int) -> models.Roster:
    db_roster = models.Roster(
        name=roster.name,
        is_active=roster.is_active,
        created_by=user_id,
        modified_by=user_id,
    )
    db.add(db_roster)
    db.commit()
    db.refresh(db_roster)
    return db_roster


def create_rosters(db: Session, rosters: list[schemas.RosterCreate], user_id: int) -> list[models.Roster]:
    db_rosters = []
    for roster in rosters:
        db_roster = create_roster(db=db, roster=roster, user_id=user_id)
        db_rosters.append(db_roster)
    return db_rosters


def get_rosters(db: Session) -> list[models.Roster]:
    return db.query(models.Roster).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()