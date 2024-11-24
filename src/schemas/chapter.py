from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .story import Story
    from .transcription import Transcription


class ChapterBase(SQLModel):
    story_id: int = Field(foreign_key="story.id")
    status: str
    title: str
    video_link: Optional[str]


class Chapter(ChapterBase, table=True):
    __tablename__: str = "chapter"

    id: Optional[int] = Field(default=None, primary_key=True)
    story: "Story" = Relationship(back_populates="chapters")
    transcription: "Transcription" = Relationship(back_populates="chapter")


class ChapterCreate(ChapterBase):
    pass


class ChapterRead(ChapterBase):
    id: int
