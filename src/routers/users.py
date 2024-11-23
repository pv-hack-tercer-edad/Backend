from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from src.config.db import get_session
from src.schemas.user import User, UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    session: Session = Depends(get_session),
):
    user = session.get(User, user_id)
    print(user)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
