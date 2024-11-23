from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.schemas.vital_signs_history import VitalSignsHistory


class VitalSignBase(SQLModel):
    id: str = Field(primary_key=True)
    label: str
    unit: str


class VitalSign(VitalSignBase, table=True):
    __tablename__: str = "vital_signs"

    vital_signs_history: List["VitalSignsHistory"] = Relationship(
        back_populates="vital_sign"
    )


class VitalSignCreate(VitalSignBase):
    pass


class VitalSignRead(VitalSignBase):
    pass
