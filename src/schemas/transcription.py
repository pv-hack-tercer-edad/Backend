from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from src.schemas.ai_scene import AIScene
    from src.schemas.chapter import Chapter


class TranscriptionBase(SQLModel):
    chapter_id: int = Field(foreign_key="chapter.id")
    content: str
    recording_link: str


class Transcription(TranscriptionBase, table=True):
    __tablename__: str = "transcription"

    id: Optional[int] = Field(default=None, primary_key=True)
    ai_scenes: List["AIScene"] = Relationship(back_populates="transcription")
    chapter: "Chapter" = Relationship(back_populates="transcription")


class TranscriptionCreate(TranscriptionBase):
    pass


class TranscriptionRead(TranscriptionBase):
    id: int
