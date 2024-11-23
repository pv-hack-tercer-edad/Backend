from pydantic import BaseModel

class Onboarding(BaseModel):
    pacient_id: int
    doctor_id: int
    preexisting_conditions: str
    treatment: str
    allergies: str
    checklist_details: list
    treatment_details: list