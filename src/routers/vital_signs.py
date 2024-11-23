from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError

from src.schemas.vital_signs import VitalSignCreate, VitalSignRead, VitalSign
from src.config.db import get_session


router = APIRouter(prefix="/vital-signs", tags=["vital-signs"])


@router.get("/", response_model=List[VitalSignRead])
def get_vital_signs(
    session: Session = Depends(get_session),
):
    vital_signs = session.exec(select(VitalSign)).all()
    if vital_signs is None:
        raise HTTPException(status_code=404, detail="Vital signs not found")
    return vital_signs


@router.get("/{vital_sign_id}", response_model=VitalSignRead)
def get_vital_sign(
    vital_sign_id: str,
    session: Session = Depends(get_session),
):
    vital_sign = session.get(VitalSign, vital_sign_id)
    if vital_sign is None:
        raise HTTPException(status_code=404, detail="Vital sign not found")
    return vital_sign


@router.post("/create", response_model=VitalSignRead)
def create_vital_sign(
    params: VitalSignCreate,
    session: Session = Depends(get_session),
):
    db_vital_sign = VitalSign.model_validate(params)
    try:
        session.add(db_vital_sign)
        session.commit()
        session.refresh(db_vital_sign)
        return db_vital_sign
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occured when creating the vital sign: {e}",
        )
