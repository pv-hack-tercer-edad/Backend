from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from src.schemas.patient import Patient

router = APIRouter(
    prefix="/onboarding",
    tags=["onboarding"],
    responses={404: {"description": "Not found"}},
)


@router.post("/new-patient", tags=["onboarding"])
def onboarding_doctor(patient: Patient):
    encoded_patient = jsonable_encoder(patient)
    print(encoded_patient)
    return {"message": "Doctor onboarding!"}
