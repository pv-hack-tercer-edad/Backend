from typing import TYPE_CHECKING, List, Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .story import Story


class UserBase(SQLModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class User(UserBase, table=True):
    __tablename__: str = "user"
    id: Optional[int] = Field(default=None, primary_key=True)

    stories: List["Story"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
