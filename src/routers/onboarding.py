from fastapi import APIRouter, Depends, HTTPException
from src.schemas.onboarding import OnboardingCreateParams, Onboarding, OnboardingRead
from src.config.db import get_session
from sqlmodel import Session
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(
    prefix="/onboarding",
    tags=["onboarding"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{onboarding_id}", response_model=OnboardingRead)
def get_ficha(
    onboarding_id: int,
    session: Session = Depends(get_session),
):
    onboarding = session.get(Onboarding, onboarding_id)
    if onboarding is None:
        raise HTTPException(status_code=404, detail="onboarding not found")
    return onboarding


@router.post("/create", response_model=OnboardingRead)
def create_onboarding(
    params: OnboardingCreateParams,
    session: Session = Depends(get_session),
):
    db_onboarding = Onboarding.model_validate(params)
    try:
        session.add(db_onboarding)
        session.commit()
        session.refresh(db_onboarding)
        return db_onboarding
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500, detail="An error occured when creating the metric"
        )
