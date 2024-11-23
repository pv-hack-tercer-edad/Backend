from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .story import Story
    from .generative_question import GenerativeQuestion


class ChapterBase(SQLModel):
    story_id: int = Field(foreign_key="story.id")
    generative_question_id: int = Field(foreign_key="generative_question.id")
    status: str
    title: str
    video_link: Optional[str]


class Chapter(ChapterBase, table=True):
    __tablename__: str = "chapter"

    id: Optional[int] = Field(default=None, primary_key=True)
    story: "Story" = Relationship(back_populates="chapters")
    generative_question: "GenerativeQuestion" = Relationship(back_populates="chapters")


class ChapterCreate(ChapterBase):
    pass


class ChapterRead(ChapterBase):
    id: int
