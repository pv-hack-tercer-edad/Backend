from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.schemas.transcription import Transcription


class AISceneBase(SQLModel):
    index: int
    image_link: str
    transcription_id: int = Field(foreign_key="transcription.id")


class AIScene(AISceneBase, table=True):
    __tablename__: str = "ai_scene"
    id: Optional[int] = Field(default=None, primary_key=True)

    transcription: "Transcription" = Relationship(back_populates="ai_scenes")


class AISceneCreate(AISceneBase):
    pass


class AISceneRead(AISceneBase):
    id: int
