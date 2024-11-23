from typing import Optional

from pydantic_extra_types.pendulum_dt import DateTime
from sqlmodel import Field, SQLModel


class ObservationBase(SQLModel):
    text: str
    img_link: str | None = None
    img_description: str | None = None
    date: DateTime


class Observation(ObservationBase, table=True):
    __tablename__: str = "observations"
    user_id: int = Field(foreign_key="user.id")

    id: Optional[int] = Field(default=None, primary_key=True)


class ObservationCreate(ObservationBase):
    pass


class ObservationRead(ObservationBase):
    id: int
    date: DateTime
