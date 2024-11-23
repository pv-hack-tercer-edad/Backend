from typing import Optional

from pydantic_extra_types.pendulum_dt import DateTime
from sqlmodel import Field, SQLModel


class ObservationBase(SQLModel):
    title: str
    description: str
    img_link: str
    created_at: DateTime
    tag: str


class Observation(ObservationBase, table=True):
    __tablename__: str = "observations"
    user_id: int = Field(foreign_key="user.id")

    id: Optional[int] = Field(default=None, primary_key=True)


class ObservationCreate(ObservationBase):
    pass


class ObservationRead(ObservationBase):
    id: int
    created_at: DateTime
