from pydantic import BaseModel


class Patient(BaseModel):
    name: str
    rut: str
    age: int
    height: int
    weight: int
    gender: str
