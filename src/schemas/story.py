from sqlalchemy import TIMESTAMP, Column, text
from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from pydantic_extra_types.pendulum_dt import DateTime

if TYPE_CHECKING:
    from .user import User
    from .chapter import Chapter


class StoryBase(SQLModel):
    title: str
    user_id: int = Field(foreign_key="user.id")


class Story(StoryBase, table=True):
    __tablename__: str = "story"
    id: Optional[int] = Field(default=None, primary_key=True)

    user: "User" = Relationship(back_populates="stories")
    chapters: List["Chapter"] = Relationship(back_populates="story")

    created_at: DateTime = Field(
        default_factory=datetime.now,
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )


class StoryCreate(StoryBase):
    pass


class StoryRead(StoryBase):
    id: int
