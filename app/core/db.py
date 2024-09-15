from fastapi import Depends
from sqlalchemy.orm import Session

from app.core import dependencies, schemas, security
from app.core.config import settings
from app.db import models, crud
from app.db.database import engine, SessionLocal
from app.db.enums import UserRole

def init_db() -> None:
    models.Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        superuser = db.query(models.User).filter(models.User.email == settings.FIRST_SUPERUSER).first()
        if superuser is None:
            superuser = schemas.UserCreate(
                email = settings.FIRST_SUPERUSER,
                password = settings.FIRST_SUPERUSER_PASSWORD,
                role = UserRole.super_admin
            )
            superuser = crud.create_user(db, superuser)
        
        election = db.query(models.Election).first()
        if election is None:
            election = schemas.ElectionCreate(
                seats_amount=settings.FIRST_ELECTION_SEATS_AMOUNT,
                is_active=True,
                user_id=superuser.id,
            )
            election = crud.create_election(db, election, user_id=superuser.id)
        
        rosters = db.query(models.Roster).all()
        if len(rosters) == 0:
            for i in range(settings.FIRST_ROSTER_AMOUNT):
                rosters.append(schemas.RosterCreate(
                    name=f'Roster {i + 1}',
                    user_id=superuser.id
                ))
            rosters = crud.create_rosters(db, rosters, user_id=superuser.id)