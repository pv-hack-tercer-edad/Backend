from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from src.schemas.story import StoryCreate, Story, StoryRead
from src.schemas.chapter import Chapter
from src.config.db import get_session

router = APIRouter(
    prefix="/stories",
    tags=["stories"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{user_id}", response_model=StoryRead)
def get_story(
    user_id: int,
    session: Session = Depends(get_session),
):
    story = session.get(Story, user_id)
    if story is None:
        raise HTTPException(status_code=404, detail="story not found")
    return story


@router.post("/create")
def create_story(
    params: StoryCreate,
    session: Session = Depends(get_session),
):

    query = select(Story).where(Story.user_id == params.user_id)
    current_story = session.scalars(query).first()
    if current_story:
        return {"story": current_story, "chapters": current_story.chapters}

    db_story = Story.model_validate(params)
    try:
        session.add(db_story)
        session.commit()
        session.refresh(db_story)

        chapters_data = [
            {"title": "Infancia", "story_id": db_story.id, "status": "WIP"},
            {"title": "Primer amor", "story_id": db_story.id, "status": "WIP"},
            {"title": "Vejez", "story_id": db_story.id, "status": "WIP"},
        ]
        db_chapters = []
        for chapter_data in chapters_data:
            chapter = Chapter(**chapter_data)
            db_chapters.append(chapter)
            db_story.chapters.append(chapter)

        session.add_all(db_chapters)
        session.commit()

        session.refresh(db_story)
        session.refresh(db_chapters)
        return {"story": db_story, "chapters": db_story.chapters}
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(
            status_code=500, detail="An error occured when creating the story"
        )
