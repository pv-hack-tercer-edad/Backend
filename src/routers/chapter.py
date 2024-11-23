from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from sqlalchemy.exc import SQLAlchemyError

from src.schemas.chapter import Chapter, ChapterCreate, ChapterRead
from src.config.db import get_session


router = APIRouter(prefix="/chapter", tags=["chapter"])


@router.get("/{chapter_id}", response_model=ChapterRead)
def get_chapter(
    chapter_id: int,
    session: Session = Depends(get_session),
):
    chapter = session.get(Chapter, chapter_id)
    print(chapter)
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter


@router.post("/create", response_model=ChapterRead)
def create_chapter(
    chapter: ChapterCreate,
    session: Session = Depends(get_session),
):
    db_chapter = Chapter.model_validate(chapter)
    try:
        session.add(db_chapter)
        session.commit()
        session.refresh(db_chapter)
        return db_chapter
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500, detail="An error occured when creating the metric"
        )
