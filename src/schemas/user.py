from typing import List, Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from src.schemas.vital_signs_history import VitalSignsHistory


class UserBase(SQLModel):
    type: str
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class User(UserBase, table=True):
    __tablename__: str = "user"
    id: Optional[int] = Field(default=None, primary_key=True)

    vital_signs_history: List["VitalSignsHistory"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
