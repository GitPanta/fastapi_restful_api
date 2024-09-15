from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base
from .enums import UserRole


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.user)


class Election(Base):
    __tablename__ = "elections"
    
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=True)
    seats_amount = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
    date_creation = Column(DateTime, nullable=False, server_default=func.now())
    date_modified = Column(DateTime, nullable=False, server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))
    modified_by = Column(Integer, ForeignKey("users.id"))
    
    results = relationship("Record", back_populates="election")


class Roster(Base):
    __tablename__ = "rosters"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
    date_creation = Column(DateTime, nullable=False, server_default=func.now())
    date_modified = Column(DateTime, nullable=False, server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))
    modified_by = Column(Integer, ForeignKey("users.id"))


class Record(Base):
    __tablename__ = "records"

    election_id = Column(Integer, ForeignKey("elections.id"), primary_key=True)
    roster_id = Column(Integer, ForeignKey("rosters.id"), primary_key=True)
    votes_amount = Column(Integer, nullable=False, default=0)
    roster_seats_amount = Column(Integer, nullable=False, default=0)
    
    election = relationship("Election", back_populates="results")