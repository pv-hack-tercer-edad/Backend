from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .chapter import Chapter


class GenerativeQuestionBase(SQLModel):
    theme: str
    content: str


class GenerativeQuestion(GenerativeQuestionBase, table=True):
    __tablename__: str = "generative_question"
    id: Optional[int] = Field(default=None, primary_key=True)

    chapters: List["Chapter"] = Relationship(back_populates="generative_question")


class GenerativeQuestionCreate(GenerativeQuestionBase):
    pass


class GenerativeQuestionRead(GenerativeQuestionBase):
    id: int
