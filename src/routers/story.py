from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from sqlalchemy.exc import SQLAlchemyError

from src.schemas.story import StoryCreate, Story, StoryRead
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


@router.post("/create", response_model=StoryRead)
def create_story(
    params: StoryCreate,
    session: Session = Depends(get_session),
):
    db_story = Story.model_validate(params)
    try:
        session.add(db_story)
        session.commit()
        session.refresh(db_story)
        return db_story
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500, detail="An error occured when creating the story"
        )
