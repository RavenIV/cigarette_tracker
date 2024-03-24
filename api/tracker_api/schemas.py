from datetime import datetime

from pydantic import BaseModel


class CigaretteBase(BaseModel):
    smoking_time: datetime


class CigaretteCreate(CigaretteBase):
    pass


class Cigarette(CigaretteBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    telegram_id: int


class UserCreate(UserBase):
    telegram_id: int


class UserDetail(UserBase):
    id: int
    date_joined: datetime
    cigarettes: list[Cigarette]

    class Config:
        orm_mode = True


class UserList(UserBase):
    id: int
    date_joined: datetime

    class Config:
        orm_mode = True
