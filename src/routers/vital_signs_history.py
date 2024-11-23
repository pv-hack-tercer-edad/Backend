from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError

from src.schemas.vital_signs_history import (
    VitalSignsHistory,
    VitalSignsHistoryCreate,
    VitalSignsHistoryRead,
)
from src.config.db import get_session


router = APIRouter(prefix="/vital-signs-history", tags=["vital-signs-history"])


@router.get("/", response_model=List[VitalSignsHistoryRead])
def get_vital_sign_histories(
    session: Session = Depends(get_session),
):
    vital_signs = session.exec(select(VitalSignsHistory)).all()
    if vital_signs is None:
        raise HTTPException(status_code=404, detail="Vital signs history not found")
    return vital_signs


@router.get("/{user_id}", response_model=List[VitalSignsHistoryRead])
def get_vital_sign_history(
    user_id: int,
    session: Session = Depends(get_session),
):
    vital_sign_history = session.exec(
        select(VitalSignsHistory).where(VitalSignsHistory.user_id == user_id)
    ).all()
    if vital_sign_history is None:
        raise HTTPException(
            status_code=404,
            detail=f"Vital sign history not found for user_id: {user_id}    ",
        )
    return vital_sign_history


@router.post("/create", response_model=VitalSignsHistoryRead)
def create_vital_sign_history(
    params: VitalSignsHistoryCreate,
    session: Session = Depends(get_session),
):
    db_vital_sign_history = VitalSignsHistory.model_validate(params)
    try:
        session.add(db_vital_sign_history)
        session.commit()
        session.refresh(db_vital_sign_history)
        return db_vital_sign_history
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occured when creating the vital sign history: {e}",
        )
