from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, desc, select
from sqlalchemy.exc import SQLAlchemyError

from src.schemas.vital_signs import VitalSign, VitalSignReadLatest
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


@router.get("/latest/{user_id}", response_model=List[VitalSignReadLatest])
def get_latest_vital_sign_history(
    user_id: int,
    session: Session = Depends(get_session),
):
    # First get all vital signs to ensure we query each one
    vital_signs = session.exec(select(VitalSign)).all()

    latest_histories = []
    for vital_sign in vital_signs:
        vital_sign_data = vital_sign.model_dump()
        # For each vital sign, get the latest history entry for this user
        query = (
            select(VitalSignsHistory)
            .where(
                VitalSignsHistory.user_id == user_id,
                VitalSignsHistory.vital_sign_id == vital_sign.id,
            )
            .order_by(desc(VitalSignsHistory.date))
            .limit(1)
        )
        latest_history = session.exec(query).first()

        latest_history_data = (
            latest_history.model_dump(include={"date", "value"})
            if latest_history
            else {"date": None, "value": None}
        )

        latest_histories.append(
            VitalSignReadLatest.model_validate(
                {**vital_sign_data, **latest_history_data}
            )
        )

    if not latest_histories:
        raise HTTPException(
            status_code=404,
            detail=f"No vital sign history found for user_id: {user_id}",
        )

    return latest_histories


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
