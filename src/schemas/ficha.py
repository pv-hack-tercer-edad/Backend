from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import BaseModel


class FichaBase(SQLModel):
    age: int
    height: int
    weight: int
    rut: str
    gender: str


class Ficha(FichaBase, table=True):
    __tablename__: str = "ficha"
    user_id: int = Field(foreign_key="user.id")

    id: Optional[int] = Field(default=None, primary_key=True)


class FichaCreate(FichaBase):
    pass


class FichaRead(FichaBase):
    id: int
    rut: str


class FichaCreateParams(BaseModel):
    age: int
    height: int
    weight: int
    rut: str
    gender: str
    user_id: int
