from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from sqlalchemy.exc import SQLAlchemyError

from src.schemas.observation import ObservationCreate, ObservationRead, Observation
from src.config.db import get_session


router = APIRouter(prefix="/observations", tags=["observations"])


@router.get("/{observation_id}", response_model=ObservationRead)
def get_observation(
    observation_id: int,
    session: Session = Depends(get_session),
):
    observation = session.get(Observation, observation_id)
    print(observation)
    if observation is None:
        raise HTTPException(status_code=404, detail="Observation not found")
    return observation


@router.post("/create", response_model=ObservationRead)
def create_observation(
    observation: ObservationCreate,
    session: Session = Depends(get_session),
):
    db_observation = Observation.model_validate(observation, update={"user_id": 1})
    try:
        session.add(db_observation)
        session.commit()
        session.refresh(db_observation)
        return db_observation
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500, detail="An error occured when creating the metric"
        )
