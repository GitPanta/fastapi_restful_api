from pydantic import BaseModel

from app.db.enums import UserRole

class ElectionBase(BaseModel):
    description: str | None = None
    seats_amount: int
    is_active: bool = True


class ElectionCreate(ElectionBase):
    pass


class Election(ElectionBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True


class ElectionRecord(BaseModel):
    roster_id: int
    roster_name: str
    roster_seats_amount: int
    roster_votes_amount: int


class ElectionResults(BaseModel):
    election_id: int
    election_seats_amount: int
    results: list[ElectionRecord]


class ElectionUpdateSeats(BaseModel):
    id: int
    seats_amount: int


class RecordBase(BaseModel):
    election_id: int
    roster_id: int
    votes_amount: int


class RecordCreate(RecordBase):
    pass


class Record(RecordCreate):
    roster_seats_amount: int


class RosterBase(BaseModel):
    name: str


class RosterCreate(RosterBase):
    is_active: bool = True


class Roster(RosterBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    role: str = UserRole.user


class User(UserBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []
