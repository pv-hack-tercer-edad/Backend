from typing import TYPE_CHECKING, Optional

from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.schemas.vital_signs import VitalSign
    from src.schemas.user import User


class VitalSignsHistoryBase(SQLModel):
    date: datetime
    value: float
    vital_sign_id: str = Field(foreign_key="vital_signs.id")
    user_id: int = Field(foreign_key="user.id")


class VitalSignsHistory(VitalSignsHistoryBase, table=True):
    __tablename__: str = "vital_signs_history"
    id: Optional[int] = Field(default=None, primary_key=True)

    vital_sign: "VitalSign" = Relationship(back_populates="vital_signs_history")
    user: "User" = Relationship(back_populates="vital_signs_history")


class VitalSignsHistoryCreate(VitalSignsHistoryBase):
    pass


class VitalSignsHistoryRead(VitalSignsHistoryBase):
    id: int
