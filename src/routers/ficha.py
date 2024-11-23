from fastapi import APIRouter, Depends, HTTPException
from src.schemas.ficha import FichaCreateParams, Ficha, FichaRead
from src.config.db import get_session
from sqlmodel import Session
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(
    prefix="/ficha",
    tags=["ficha"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{ficha_id}", response_model=FichaRead)
def get_ficha(
    ficha_id: int,
    session: Session = Depends(get_session),
):
    ficha = session.get(Ficha, ficha_id)
    if ficha is None:
        raise HTTPException(status_code=404, detail="ficha not found")
    return ficha


@router.post("/create", response_model=FichaRead)
def create_ficha(
    params: FichaCreateParams,
    session: Session = Depends(get_session),
):
    db_ficha = Ficha.model_validate(params)
    try:
        session.add(db_ficha)
        session.commit()
        session.refresh(db_ficha)
        return db_ficha
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500, detail="An error occured when creating the metric"
        )
