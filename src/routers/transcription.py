from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from sqlalchemy.exc import SQLAlchemyError

from src.schemas.transcription import (
    TranscriptionCreate,
    Transcription,
    TranscriptionRead,
)
from src.config.db import get_session

router = APIRouter(
    prefix="/transcription",
    tags=["transcription"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{transcription_id}", response_model=TranscriptionRead)
def get_transcription(
    transcription_id: int,
    session: Session = Depends(get_session),
):
    transcription = session.get(Transcription, transcription_id)
    if transcription is None:
        raise HTTPException(status_code=404, detail="transcription not found")
    return transcription


@router.post("/create", response_model=TranscriptionRead)
def create_transcription(
    params: TranscriptionCreate,
    session: Session = Depends(get_session),
):
    db_transcription = Transcription.model_validate(params)
    try:
        session.add(db_transcription)
        session.commit()
        session.refresh(db_transcription)
        return db_transcription
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500, detail="An error occured when creating the transcription"
        )
