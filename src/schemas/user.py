from typing import Optional

from pendulum import now
from pydantic import EmailStr
from pydantic_extra_types.pendulum_dt import DateTime
from sqlmodel import Field, SQLModel, Column, TIMESTAMP, text


class UserBase(SQLModel):
    type: str
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class User(UserBase, table=True):
    __tablename__: str = "user"
    id: Optional[int] = Field(default=None, primary_key=True)


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
