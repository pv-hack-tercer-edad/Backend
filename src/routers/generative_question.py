from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from src.schemas.generative_question import GenerativeQuestion
from src.config.db import get_session


router = APIRouter(prefix="/generative-questions", tags=["generative-questions"])


@router.get("/", response_model=List[GenerativeQuestion])
def get_generative_questions(
    session: Session = Depends(get_session),
):
    questions = session.exec(select(GenerativeQuestion)).all()
    if not questions:
        raise HTTPException(status_code=404, detail="No generative questions found")
    return questions
