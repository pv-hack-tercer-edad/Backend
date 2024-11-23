from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError

from src.schemas.ai_scene import (
    AIScene,
    AISceneCreate,
    AISceneRead,
)
from src.config.db import get_session


router = APIRouter(prefix="/ai-scene", tags=["ai-scene"])


@router.get("/{ai_scene_id}", response_model=AISceneRead)
def get_ai_scene(
    ai_scene_id: int,
    session: Session = Depends(get_session),
):
    ai_scene = session.exec(select(AIScene).where(AIScene.id == ai_scene_id)).all()
    if ai_scene is None:
        raise HTTPException(
            status_code=404,
            detail=f"AI scene with id {ai_scene_id} not found",
        )
    return ai_scene


@router.post("/create", response_model=AISceneRead)
def create_vital_sign_history(
    params: AISceneCreate,
    session: Session = Depends(get_session),
):
    db_ai_scene = AISceneCreate.model_validate(params)
    try:
        session.add(db_ai_scene)
        session.commit()
        session.refresh(db_ai_scene)
        return db_ai_scene
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occured when creating the ai scene: {e}",
        )
