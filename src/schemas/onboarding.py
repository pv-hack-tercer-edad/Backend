from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import Optional
from pydantic_extra_types.pendulum_dt import DateTime


class OnboardingBase(SQLModel):
    patient_id: int
    doctor_id: int
    preexisting_conditions: str
    treatment: str
    allergies: str
    date: DateTime


class Onboarding(OnboardingBase, table=True):
    __tablename__: str = "onboarding"
    id: Optional[int] = Field(default=None, primary_key=True)


class OnboardingCreate(OnboardingBase):
    pass


class OnboardingRead(OnboardingBase):
    id: int


class OnboardingCreateParams(BaseModel):
    patient_id: int
    doctor_id: int
    preexisting_conditions: str
    treatment: str
    allergies: str
    date: DateTime
